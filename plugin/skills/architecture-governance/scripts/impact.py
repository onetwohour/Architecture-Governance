#!/usr/bin/env python3
"""Conservative reverse-owner dependency and probe traceability query.

A missing graph edge can hide real impact. This is a navigation aid, not an
authoritative affected-test selector.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

from project_state import compile_state, git_status, note_adapter, source_tests


def impact(raw, owner_ids, locations):
    owners = {x["id"]: x for x in raw.get("owners", [])}
    unknown = sorted(set(owner_ids) - set(owners))
    if unknown:
        raise ValueError("unknown owner(s): " + ", ".join(unknown))
    reverse = defaultdict(set)
    for owner in owners.values():
        for dep in owner.get("depends_on", []):
            reverse[dep].add(owner["id"])
    affected = set(owner_ids)
    pending = list(owner_ids)
    while pending:
        for dependent in sorted(reverse[pending.pop()]):
            if dependent not in affected:
                affected.add(dependent)
                pending.append(dependent)
    probes = sorted(
        p["id"] for p in raw.get("probes", [])
        if set(p.get("owners", [])).intersection(affected)
    )
    contracts = sorted(
        c["id"] for c in raw.get("contracts", [])
        if c.get("owner") in affected
        or set(c.get("mandatory_probes", [])).intersection(probes)
    )
    return {
        "input_owners": sorted(set(owner_ids)), "affected_owners": sorted(affected),
        "candidate_contracts": contracts, "candidate_probes": probes,
        "probe_marker_locations": {pid: locations.get(pid, []) for pid in probes},
        "proof_scope": "transitive reverse declared owner-dependencies and explicit probe ownership",
        "does_not_prove": "complete runtime impact, runnable tests, or required validation sufficiency"
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--adapter", choices=["the-note"])
    src.add_argument("--input", type=Path)
    parser.add_argument("--owner", required=True, action="append")
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve()
        warnings = []
        raw = note_adapter(root, warnings) if args.adapter else json.loads(args.input.read_text(encoding="utf-8"))
        state, errors = compile_state(raw, git=git_status(root))
        errors += warnings
        if errors:
            for error in errors:
                print("ERROR: " + error, file=sys.stderr)
            return 2
        locations = source_tests(root) if args.adapter else {}
        print(json.dumps(impact(raw, args.owner, locations),
                         indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
