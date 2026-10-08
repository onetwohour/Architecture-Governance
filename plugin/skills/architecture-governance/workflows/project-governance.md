# Project governance: make status a projection, not another owner

**When to load:** a project is accumulating large STATUS/TODO files, duplicated defects, opaque probe locations, untrustworthy readiness labels, or multiple incompatible tracking registries. Also load `references/writing.md`, `references/evidence.md` and `references/delivery.md`.

## Start with the ownership question

A long STATUS.md is a **symptom**, not automatically a design defect. First distinguish:
- Normative contracts: define what must be true (owner document, declared dependencies).
- Probe requirements: define what to challenge (probe catalog).
- Test implementations: contain executable assertions (crate-local code).
- Execution evidence: records what actually ran at a revision/platform/working tree.
- Issue/work records: track human-chosen work, priority and unresolved defects.
- Generated views: summarize authoritative sources; never become independent truth.

If the project already has registries, **read them**; never introduce a parallel governance database merely to produce a dashboard.

## Migration workflow

1. **Inventory without changing sources.** Read every STATUS/TODO item, attach provenance, and classify: durable implementation fact, open defect, planned task, probe, readiness claim, validation observation, descriptive narrative. Identify duplication and omissions. Protect original content until reconciled.
2. **Allocate single ownership.** Existing owner documents own semantics; probe registries own requirements; run records own observed results; issue/work tracking owns human decisions. A tool's derived IR is read-only and rebuildable.
3. **Design a project adapter, not a second schema of meaning.** If the project has machine-readable registries, map directly to the normalized projection format. If it does not, define a minimal export at the existing owner rather than fabricating architecture from filenames.
4. **Reconcile issue lifecycle.** A resolved defect is not automatically verified readiness. Do not duplicate missing mandatory probes as independent manual TODO tasks. Preserve mapping from each migrated item to its source and owner.
5. **Link requirements to evidence.** Probe declaration, source marker/location, test execution and semantic-coverage review are different facts. Only the appropriate authority may promote readiness; the compiler must not infer semantic correctness from command exit 0.
6. **Compile read-only first.** Use `scripts/project_state.py` to validate references and generate side-by-side projections. Review the derived TODO/STATUS against the originals before retiring manual content.
7. **Switch authority in one reviewed migration.** Only after full source-to-destination reconciliation should root STATUS/TODO become generated outputs. Add target-repo CI freshness checks and remove manual status update obligations.
8. **Prove the migration.** Delete *only generated copies*, rebuild deterministically, mutate evidence to stale/failure, inject unknown owner/probe, and ensure the compiler refuses inconsistencies or lowers observed confidence.

## Portable compiler

Python 3.11+:

```bash
python scripts/project_state.py --root /repo --adapter the-note --out /tmp/generated --write
python scripts/project_state.py --root /repo --adapter the-note --out /tmp/generated --check
```

The built-in `the-note` adapter reads the project's existing `docs/architecture.toml`, `docs/quality/probes.toml`, `docs/quality/readiness.toml`, and Rust probe markers. It **does not modify The Note** and does not own its design. The Note adapter provides a useful projection of these sources, not full feature completion or semantic coverage.

Other projects can export a normalized JSON snapshot from **their own** registries:

```bash
python scripts/project_state.py --root /repo --input /tmp/project-snapshot.json --out /tmp/generated --write
```

Optional `--issues /path/tracking.toml` accepts target-owned `[[issue]]` and `[[work]]` records; `--evidence-dir` reads captured runner JSON with probe IDs in `label`. The JSON input and `project-state.json` are exchange/projection formats, **not** alternate sources of truth. See `references/project-state-format.md`.

Only explicit `--write` writes files; the compiler never writes root STATUS.md/TODO.md. `--check` detects stale generated outputs. It validates IDs and references, not owner-document semantics. If the target uses other schemas, write an adapter; do not deform its normative owners to fit this tool.

## Release gate

A status compiler is complete only when all source facts are accounted for, no duplicate authority was created, outputs are deterministically regenerated, and the evidence-to-readiness proof boundary is explicit. When manual semantics review is outstanding, output REVIEW_REQUIRED or UNKNOWN, never a fabricated PASS.
