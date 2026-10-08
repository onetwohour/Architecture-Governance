# Project State compiler exchange format

> NON-NORMATIVE. This document specifies an optional **tool input/export format**, not a target project's architecture or issue registry.

The compiler consumes the target's existing authoritative sources. Never manually maintain the normalized JSON alongside those sources. Export it afresh from a project-owned adapter when needed.

## Normalized JSON

```json
{
  "project": "example",
  "owners": [
    {"id": "runtime", "path": "docs/runtime.md", "depends_on": []}
  ],
  "probes": [
    {"id": "P-001", "owners": ["runtime"], "cases": ["crash"], "stage": 2}
  ],
  "contracts": [
    {
      "id": "runtime.recovery",
      "owner": "runtime",
      "declared_readiness": "DRAFT",
      "mandatory_probes": ["P-001"],
      "source_evidence_paths": []
    }
  ]
}
```

No document semantic text is copied into the snapshot. IDs link back to the existing owners, and claims are explicitly labeled as imported claims. `probes[].cases` is a display hint; the current compiler checks duplicate case IDs but does not infer whether a test covers a case.

### Optional Issue TOML

```toml
[[issue]]
id = "SD-001"
kind = "SPEC_DEFECT"
state = "OPEN"
owner = "runtime"
summary = "Recovery terminal is unspecified"
contracts = ["runtime.recovery"]
```

Allowed kinds: `SPEC_DEFECT`, `IMPLEMENTATION_DEFECT`, `IMPLEMENTATION_GAP`, `VALIDATION_GAP`, `PERFORMANCE`, `TASK`. Allowed states: `OPEN`, `IN_PROGRESS`, `BLOCKED`, `RESOLVED`, `CLOSED`. These are **optional tracking metadata**, not specifications. Only import issues actually owned by the target project; don't manufacture a new file merely for this compiler.

### Evidence import

The compiler accepts JSON files emitted by `run_validation.py`. A record's `label` must match a registered Probe ID. Revision and clean-worktree matching determine whether an execution record is current enough to display PASS/FAIL, but **neither PASS nor matching revision proves a Probe's full semantic contract**. Imported evidence files can be forged; use project CI provenance if the distinction matters.

The current compiler reports:
- `implementation: LOCATED/UNKNOWN`: source marker locations, never runnable-test certification.
- `execution: COMMAND_PASS/COMMAND_FAIL/UNKNOWN/STALE`: labelled individual-command results, not proof the command actually tests the Probe.
- `execution_assessment: BLOCKED/STALE/UNKNOWN/REVIEW_REQUIRED`: summary across required probes.
- `semantic_readiness: NOT_ASSESSED`: deliberate. The project remains responsible for verifying normative conformance.

`--out` writes only `project-state.json`, `STATUS.generated.md`, `TODO.generated.md` when `--write` is explicitly supplied. Generated content is a navigational/reporting artifact. Do not treat the file `STATUS.generated.md` as the target's authoritative status until the target's own migration and CI freshness checks are in place.

## Proof and limits

The validator detects missing/duplicate source references, not contradictions in the meaning of normative prose. It does not parse or run arbitrary test targets from a marker, authenticate evidence, run adversarial security tests, certify readiness, or infer a source file's implementation status.
