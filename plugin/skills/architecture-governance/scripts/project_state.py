#!/usr/bin/env python3
"""Read-only source adapter and derived project-state compiler.

Inputs remain authoritative in the target project. Output is a projection, not a
new registry or a proof of semantic correctness. Standard library Python 3.11+.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib

PROBE_MARKER = re.compile(r"//\s*probe:\s*(P-\d{3})\b")
CLOSED_ISSUES = {"RESOLVED", "CLOSED"}
VALID_ISSUES = {"OPEN", "IN_PROGRESS", "BLOCKED", "RESOLVED", "CLOSED"}
VALID_KINDS = {
    "SPEC_DEFECT", "IMPLEMENTATION_DEFECT", "IMPLEMENTATION_GAP",
    "VALIDATION_GAP", "PERFORMANCE", "TASK"
}
GENERATED_HEADER = "<!-- GENERATED: derived projection; do not edit as a source of truth. -->\n"


def read_toml(path):
    with path.open("rb") as handle:
        return tomllib.load(handle)


def git_status(root):
    def call(*args):
        proc = subprocess.run(["git", "-C", str(root), *args],
                              text=True, capture_output=True, check=False)
        if proc.returncode:
            return None
        return proc.stdout.strip()
    return {"revision": call("rev-parse", "HEAD"),
            "dirty": bool(call("status", "--porcelain=v1", "--untracked-files=all"))
            if call("rev-parse", "HEAD") else None}


def unique_map(items, label, errors):
    result = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            errors.append(f"{label}: missing or invalid id")
            continue
        if item["id"] in result:
            errors.append(f"{label}: duplicate id {item['id']}")
        else:
            result[item["id"]] = item
    return result


def note_adapter(root, errors):
    docs = root / "docs"
    arch = read_toml(docs / "architecture.toml")
    probes = read_toml(docs / "quality" / "probes.toml")
    readiness = read_toml(docs / "quality" / "readiness.toml")
    owners = []
    for d in arch.get("document", []):
        owners.append({"id": d["id"], "path": "docs/" + d["path"],
                       "depends_on": d.get("depends_on", [])})
        if not (docs / d["path"]).is_file():
            errors.append(f"owner {d['id']}: missing document {d['path']}")
    normalized_probes = []
    for p in probes.get("probe", []):
        normalized_probes.append({
            "id": p["id"], "owners": p.get("owners", []),
            "cases": [case.get("id") for case in p.get("case", [])],
            "stage": p.get("required_before_stage")
        })
    contracts = []
    for c in readiness.get("contract", []):
        contracts.append({"id": c["id"], "owner": c["owner"],
                          "declared_readiness": c.get("state", "UNKNOWN"),
                          "mandatory_probes": c.get("mandatory_probes", []),
                          "source_evidence_paths": c.get("evidence", [])})
    return {"project": root.name, "owners": owners, "probes": normalized_probes,
            "contracts": contracts}


def source_tests(root):
    """Discover markers as hints, never as execution evidence."""
    found = defaultdict(list)
    for workspace in ("core-repo", "note-repo"):
        base = root / workspace
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.rs")):
            if any(piece in ("target", ".git") for piece in path.relative_to(base).parts):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeError:
                continue
            for marker in set(PROBE_MARKER.findall(text)):
                found[marker].append(path.relative_to(root).as_posix())
    return {key: sorted(set(value)) for key, value in found.items()}


def read_issues(path):
    if path is None:
        return []
    raw = read_toml(path)
    if "issue" not in raw or not isinstance(raw["issue"], list):
        raise ValueError("issue file must contain [[issue]] records")
    return raw["issue"]


def evidence_files(folder, errors):
    if folder is None:
        return []
    if not folder.is_dir():
        errors.append(f"evidence directory does not exist: {folder}")
        return []
    records = []
    for path in sorted(folder.glob("*.json")):
        try:
            row = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(row, dict):
                raise ValueError("not an object")
            row = dict(row)
            row["_source"] = str(path)
            records.append(row)
        except (ValueError, UnicodeError) as exc:
            errors.append(f"bad evidence {path}: {exc}")
    return records


def evidence_state(record, git):
    """Execution evidence is not equivalent to normative-contract validation."""
    if not record:
        return "UNKNOWN"
    before, after = record.get("git_before", {}), record.get("git_after", {})
    if not isinstance(before, dict) or not isinstance(after, dict):
        return "UNKNOWN"
    if not git["revision"] or git["dirty"] is not False:
        return "STALE"
    if (before.get("revision") != git["revision"]
            or after.get("revision") != git["revision"]
            or before.get("worktree_dirty") is not False
            or after.get("worktree_dirty") is not False):
        return "STALE"
    if record.get("result") == "FAIL" and isinstance(record.get("exit_code"), int):
        return "FAIL"
    if (record.get("result") == "PASS" and record.get("exit_code") == 0
            and isinstance(record.get("command_argv"), list)
            and record["command_argv"]):
        return "PASS"
    return "UNKNOWN"


def compile_state(raw, *, git, markers=None, issues=None, evidence=None):
    """Pure state calculation; returns (state, structural_errors)."""
    errors = []
    owners = unique_map(raw.get("owners", []), "owner", errors)
    probes = unique_map(raw.get("probes", []), "probe", errors)
    contracts = unique_map(raw.get("contracts", []), "contract", errors)
    issue_map = unique_map(issues or [], "issue", errors)
    markers = markers or {}
    evidence = evidence or []

    for oid, owner in owners.items():
        for dep in owner.get("depends_on", []):
            if dep not in owners:
                errors.append(f"owner {oid}: unknown dependency {dep}")
    # The semantic owner-dependency registry is a DAG; report a cycle explicitly.
    visiting, visited, chain = set(), set(), []
    def visit_owner(oid):
        if oid in visiting:
            errors.append("owner dependency cycle: " + " -> ".join(chain[chain.index(oid):] + [oid]))
            return
        if oid in visited:
            return
        visiting.add(oid)
        chain.append(oid)
        for dep in sorted(owners[oid].get("depends_on", [])):
            if dep in owners:
                visit_owner(dep)
        chain.pop()
        visiting.remove(oid)
        visited.add(oid)
    for oid in sorted(owners):
        visit_owner(oid)
    for pid, probe in probes.items():
        for oid in probe.get("owners", []):
            if oid not in owners:
                errors.append(f"probe {pid}: unknown owner {oid}")
        cases = probe.get("cases", [])
        if len(cases) != len(set(cases)):
            errors.append(f"probe {pid}: duplicate case ID")
    for cid, contract in contracts.items():
        if contract.get("owner") not in owners:
            errors.append(f"contract {cid}: unknown owner {contract.get('owner')}")
        for pid in contract.get("mandatory_probes", []):
            if pid not in probes:
                errors.append(f"contract {cid}: unknown mandatory probe {pid}")
    for iid, issue in issue_map.items():
        if issue.get("owner") not in owners:
            errors.append(f"issue {iid}: unknown owner {issue.get('owner')}")
        if issue.get("kind") not in VALID_KINDS:
            errors.append(f"issue {iid}: invalid kind {issue.get('kind')}")
        if issue.get("state") not in VALID_ISSUES:
            errors.append(f"issue {iid}: invalid state {issue.get('state')}")
        if not isinstance(issue.get("summary"), str) or not issue["summary"].strip():
            errors.append(f"issue {iid}: missing summary")
        for cid in issue.get("contracts", []):
            if cid not in contracts:
                errors.append(f"issue {iid}: unknown contract {cid}")

    # Evidence labels are declared test/probe identifiers, never inferred from filenames.
    by_probe = defaultdict(list)
    for record in evidence:
        label = record.get("label")
        if label not in probes:
            errors.append(f"evidence {record.get('_source', '?')}: unknown probe label {label}")
        else:
            by_probe[label].append(record)
    result_probes = []
    for pid, probe in sorted(probes.items()):
        candidates = sorted(by_probe[pid], key=lambda x: str(x.get("ended_at_utc", "")))
        latest = candidates[-1] if candidates else None
        execution = evidence_state(latest, git)
        locations = sorted(set(markers.get(pid, [])))
        result_probes.append({
            "id": pid, "owners": sorted(set(probe.get("owners", []))),
            "stage": probe.get("stage"), "cases": probe.get("cases", []),
            "locations": locations,
            "implementation": "LOCATED" if locations else "UNKNOWN",
            "execution": execution,
            "evidence": latest.get("_source") if latest else None,
            "proof_limit": "marker is not an executable test; command success is not semantic closure"
        })
    by_id = {p["id"]: p for p in result_probes}
    result_contracts = []
    for cid, contract in sorted(contracts.items()):
        required = contract.get("mandatory_probes", [])
        statuses = [by_id[pid]["execution"] for pid in required if pid in by_id]
        # Report imported readiness as a CLAIM, not verified by the compiler.
        assessment = ("BLOCKED" if "FAIL" in statuses else
                      "STALE" if "STALE" in statuses else
                      "UNKNOWN" if not required or "UNKNOWN" in statuses else
                      "REVIEW_REQUIRED")
        result_contracts.append({
            "id": cid, "owner": contract.get("owner"),
            "declared_readiness": contract.get("declared_readiness", "UNKNOWN"),
            "mandatory_probes": required,
            "execution_assessment": assessment,
            "source_evidence_paths": contract.get("source_evidence_paths", []),
            "semantic_readiness": "NOT_ASSESSED"
        })
    open_issues = sorted(
        ({"id": i, "kind": issue["kind"], "owner": issue["owner"],
          "summary": issue["summary"], "state": issue["state"]}
         for i, issue in issue_map.items()
         if issue.get("state") not in CLOSED_ISSUES),
        key=lambda x: x["id"]
    )
    state = {
        "schema_version": 1,
        "project": raw.get("project", "unknown"),
        "git": git,
        "summary": {"owners": len(owners), "contracts": len(contracts),
                    "probes": len(probes), "located_probes": sum(bool(p["locations"]) for p in result_probes),
                    "executed_pass_probes": sum(p["execution"] == "PASS" for p in result_probes),
                    "open_issues": len(open_issues)},
        "probes": result_probes, "contracts": result_contracts, "open_issues": open_issues,
        "limitations": [
            "Source paths and probe markers do not establish executable or semantic coverage.",
            "Execution PASS concerns only an observed command, not a contract or a whole system.",
            "Imported readiness is a source claim, not re-certified by this compiler.",
            "Evidence JSON is not cryptographically authenticated; CI provenance must be validated separately.",
            "A dirty worktree invalidates reuse of clean-commit evidence."
        ],
    }
    return state, sorted(set(errors))


def md_cell(value):
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").replace("`", "\\`")


def render_status(state):
    s = state["summary"]
    lines = [GENERATED_HEADER.rstrip(), "# Project status (derived, non-normative)", "",
             f"Project: `{state['project']}`",
             f"Revision: `{state['git']['revision'] or 'UNKNOWN'}`; dirty: `{state['git']['dirty']}`", "",
             f"Owners: {s['owners']} · Contracts: {s['contracts']} · Probes: {s['probes']}",
             f"Probe markers located: {s['located_probes']} · Current clean execution PASS: {s['executed_pass_probes']}",
             f"Open issues: {s['open_issues']}", "",
             "Contract execution assessment is **not** semantic readiness.", "",
             "| Contract | Declared readiness | Execution assessment |",
             "| --- | --- | --- |"]
    for c in state["contracts"]:
        lines.append(f"| `{md_cell(c['id'])}` | {md_cell(c['declared_readiness'])} | {md_cell(c['execution_assessment'])} |")
    lines += ["", "See project-state.json for evidence/probe locations and proof limits.", ""]
    return "\n".join(lines)


def render_todo(state):
    lines = [GENERATED_HEADER.rstrip(), "# Outstanding work (derived, non-normative)", "",
             "Missing evidence is a verification task, **not** proof of a broken implementation.", "",
             "## Open tracked issues", ""]
    if not state["open_issues"]:
        lines.append("No imported open issues.")
    else:
        for issue in state["open_issues"]:
            lines.append(f"- [ ] `{md_cell(issue['id'])}` ({md_cell(issue['kind'])}; {md_cell(issue['owner'])}): {md_cell(issue['summary'])}")
    lines += ["", "## Unverified contract execution", ""]
    for c in state["contracts"]:
        if c["execution_assessment"] != "REVIEW_REQUIRED":
            lines.append(f"- [ ] `{md_cell(c['id'])}`: {md_cell(c['execution_assessment'])} (declared {md_cell(c['declared_readiness'])})")
        else:
            lines.append(f"- [ ] `{md_cell(c['id'])}`: execution PASS for listed probes; semantic review still required")
    lines += ["", "## Probe implementation-location gaps", ""]
    missing = [p["id"] for p in state["probes"] if not p["locations"]]
    lines += [f"- [ ] `{pid}`: no probe marker located (not proof of missing test)" for pid in missing]
    if not missing:
        lines.append("None found.")
    lines.append("")
    return "\n".join(lines)


def outputs(state):
    return {
        "project-state.json": json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        "STATUS.generated.md": render_status(state),
        "TODO.generated.md": render_todo(state),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--adapter", choices=["the-note"])
    src.add_argument("--input", type=Path, help="Normalized JSON exported from existing project authorities")
    parser.add_argument("--issues", type=Path, help="Optional TOML [[issue]] registry owned by target project")
    parser.add_argument("--evidence-dir", type=Path, help="Optional captured command evidence JSON directory")
    parser.add_argument("--out", type=Path, help="Output directory, not original STATUS/TODO")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.write and args.check:
        parser.error("choose --write or --check")
    if (args.write or args.check) and not args.out:
        parser.error("--out is required for --write/--check")
    try:
        root = args.root.resolve()
        errors = []
        raw = note_adapter(root, errors) if args.adapter else json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError("normalized input must be a JSON object")
        state, structural = compile_state(
            raw, git=git_status(root), markers=source_tests(root) if args.adapter else {},
            issues=read_issues(args.issues),
            evidence=evidence_files(args.evidence_dir, errors)
        )
        errors.extend(structural)
        if errors:
            for error in sorted(set(errors)):
                print("ERROR: " + error, file=sys.stderr)
            return 2
        artifacts = outputs(state)
        if args.out:
            out = args.out.resolve()
            if out in (root, root / "docs") and args.write:
                raise ValueError("refusing to write generated artifacts into the repository root or docs root")
            if args.write:
                out.mkdir(parents=True, exist_ok=True)
                for name, content in artifacts.items():
                    (out / name).write_text(content, encoding="utf-8")
            if args.check:
                mismatches = [name for name, content in artifacts.items()
                              if not (out / name).is_file()
                              or (out / name).read_text(encoding="utf-8") != content]
                if mismatches:
                    print("STALE_OUTPUT: " + ", ".join(mismatches), file=sys.stderr)
                    return 1
        print(json.dumps({"result": "PASS", "summary": state["summary"],
                          "proof_scope": "source reference validation and derived status only",
                          "semantic_readiness": "NOT_ASSESSED"}, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, tomllib.TOMLDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
