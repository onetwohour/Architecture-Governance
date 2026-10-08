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
CLOSED_WORK = {"DONE", "CANCELLED"}
VALID_WORK_STATES = {"OPEN", "IN_PROGRESS", "BLOCKED", "DONE", "CANCELLED"}
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


def read_tracking(path):
    if path is None:
        return [], []
    raw = read_toml(path)
    if not isinstance(raw.get("issue", []), list) or not isinstance(raw.get("work", []), list):
        raise ValueError("tracking file must contain [[issue]] / [[work]] arrays")
    if not raw.get("issue") and not raw.get("work"):
        raise ValueError("tracking file must contain at least one [[issue]] or [[work]]")
    return raw.get("issue", []), raw.get("work", [])


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
        return "COMMAND_FAIL"
    if (record.get("result") == "PASS" and record.get("exit_code") == 0
            and isinstance(record.get("command_argv"), list)
            and record["command_argv"]):
        return "COMMAND_PASS"
    return "UNKNOWN"


def compile_state(raw, *, git, markers=None, issues=None, work_items=None, evidence=None):
    """Pure state calculation; returns (state, structural_errors)."""
    errors = []
    owners = unique_map(raw.get("owners", []), "owner", errors)
    probes = unique_map(raw.get("probes", []), "probe", errors)
    contracts = unique_map(raw.get("contracts", []), "contract", errors)
    issue_map = unique_map(issues or [], "issue", errors)
    works = unique_map(work_items or [], "work", errors)
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

    for wid, work in works.items():
        if work.get("owner") not in owners:
            errors.append(f"work {wid}: unknown owner {work.get('owner')}")
        if work.get("state") not in VALID_WORK_STATES:
            errors.append(f"work {wid}: invalid state {work.get('state')}")
        if not isinstance(work.get("summary"), str) or not work["summary"].strip():
            errors.append(f"work {wid}: missing summary")
        if "priority" in work and (type(work["priority"]) is not int or work["priority"] < 0):
            errors.append(f"work {wid}: priority must be a nonnegative integer")
        for iid in work.get("issues", []):
            if iid not in issue_map:
                errors.append(f"work {wid}: unknown issue {iid}")
        for dep in work.get("blocked_by", []):
            if dep not in works:
                errors.append(f"work {wid}: unknown blocking work {dep}")

    # Work dependencies must not deadlock through cycles.
    visiting_work, visited_work, work_chain = set(), set(), []
    def visit_work(wid):
        if wid in visiting_work:
            errors.append("work dependency cycle: " +
                          " -> ".join(work_chain[work_chain.index(wid):] + [wid]))
            return
        if wid in visited_work:
            return
        visiting_work.add(wid)
        work_chain.append(wid)
        for dep in sorted(works[wid].get("blocked_by", [])):
            if dep in works:
                visit_work(dep)
        work_chain.pop()
        visiting_work.remove(wid)
        visited_work.add(wid)
    for wid in sorted(works):
        visit_work(wid)

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
        assessment = ("BLOCKED" if "COMMAND_FAIL" in statuses else
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
    open_work = sorted(
        ({"id": wid, "summary": work["summary"], "owner": work["owner"],
          "state": work["state"], "priority": work.get("priority"),
          "issues": sorted(set(work.get("issues", []))),
          "blocked_by": sorted(set(work.get("blocked_by", [])))}
         for wid, work in works.items()
         if work.get("state") not in CLOSED_WORK),
        key=lambda w: (w["priority"] if w["priority"] is not None else 999999,
                       w["id"])
    )
    state = {
        "schema_version": 1,
        "project": raw.get("project", "unknown"),
        "git": git,
        "summary": {"owners": len(owners), "contracts": len(contracts),
                    "probes": len(probes), "located_probes": sum(bool(p["locations"]) for p in result_probes),
                    "associated_command_passes": sum(p["execution"] == "COMMAND_PASS" for p in result_probes),
                    "open_issues": len(open_issues), "open_work_items": len(open_work)},
        "probes": result_probes, "contracts": result_contracts,
        "open_issues": open_issues, "open_work_items": open_work,
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
             f"Probe markers located: {s['located_probes']} · Current labelled command successes: {s['associated_command_passes']}",
             f"Open issues: {s['open_issues']} · Open work items: {s['open_work_items']}", "",
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
             "## Open work items", ""]
    if not state["open_work_items"]:
        lines.append("No imported open work items.")
    for work in state["open_work_items"]:
        blockers = ", ".join(work["blocked_by"]) or "none"
        issue_refs = ", ".join(work["issues"]) or "none"
        lines.append(f"- [ ] `{md_cell(work['id'])}` [{md_cell(work['state'])}] "
                     f"priority={md_cell(work['priority'])}; owner={md_cell(work['owner'])}: "
                     f"{md_cell(work['summary'])} (issues: {md_cell(issue_refs)}; "
                     f"blocked by: {md_cell(blockers)})")
    linked = {iid for work in state["open_work_items"] for iid in work["issues"]}
    uncovered = [issue for issue in state["open_issues"] if issue["id"] not in linked]
    lines += ["", "## Open issues without an open work item", ""]
    if not uncovered:
        lines.append("None.")
    for issue in uncovered:
        lines.append(f"- [ ] `{md_cell(issue['id'])}` "
                     f"({md_cell(issue['kind'])}; {md_cell(issue['owner'])}): "
                     f"{md_cell(issue['summary'])}")
    lines += ["", "## Unverified contract execution", ""]
    for c in state["contracts"]:
        if c["execution_assessment"] != "REVIEW_REQUIRED":
            lines.append(f"- [ ] `{md_cell(c['id'])}`: {md_cell(c['execution_assessment'])} "
                         f"(declared {md_cell(c['declared_readiness'])})")
        else:
            lines.append(f"- [ ] `{md_cell(c['id'])}`: labelled commands passed; "
                         "actual probe coverage and semantic review still required")
    lines += ["", "## Probe implementation-location gaps", ""]
    missing = [p["id"] for p in state["probes"] if not p["locations"]]
    lines += [f"- [ ] `{md_cell(pid)}`: no probe marker located (not proof of missing test)"
              for pid in missing]
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
    parser.add_argument("--issues", type=Path, help="Optional target-owned TOML [[issue]] and [[work]] records")
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
        issue_rows, work_rows = read_tracking(args.issues)
        state, structural = compile_state(
            raw, git=git_status(root), markers=source_tests(root) if args.adapter else {},
            issues=issue_rows, work_items=work_rows,
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
