# Optional tools

This page describes the command-line helpers included with Architecture Governance. They are **optional**: invoking the Claude Code skill does not automatically run these scripts or install hooks.

The examples below use a local checkout of this repository. Replace `/path/to/project` with the target repository.

## Prerequisites

- Python **3.11 or newer** (the project-state compiler uses `tomllib`)
- Git
- No third-party Python packages

From this repository, the scripts are under `plugin/skills/architecture-governance/scripts/`. Commands below use that path as `$SCRIPTS` for readability:

```bash
SCRIPTS=plugin/skills/architecture-governance/scripts
```

## Inspect planned vs. actual file changes

`change_scope.py` compares a temporary scope plan to tracked, staged, unstaged, and nonignored untracked files.

Example plan (`/tmp/change-scope.json`):

```json
{
  "allowed_paths": ["src/**", "tests/**"],
  "protected_paths": ["STATUS.md", "TODO.md"]
}
```

```bash
python "$SCRIPTS/change_scope.py" --repo /path/to/project --plan /tmp/change-scope.json --base HEAD
```

Exit statuses: `0` = paths within plan; `1` = protected path changed; `2` = unexpected paths require review; `3` = tool error. Only declare paths protected when they are genuinely generated or restricted in the target project.

**Limit:** This tool compares file paths, not code semantics. A change within an allowed path can still violate architecture. Broad globs should be reviewed carefully.

## Execute a command and record its result

`run_validation.py` runs a command directly (without a shell) and records exit status, Git revision, working-tree state, platform, and bounded output.

```bash
python "$SCRIPTS/run_validation.py" \
  --repo /path/to/project \
  --label unit-tests \
  --output /tmp/unit-tests.json \
  -- python -m unittest discover -s tests
```

The label is chosen by the caller; it does not establish that the command covers a particular contract. A successful command establishes only that this command exited successfully on the observed working tree. Dirty-tree evidence is not a reusable certificate for a clean commit. Evidence JSON is not authenticated and should not be treated as trusted CI attestation.

The helper does not substitute for the target project's real tests, architecture gates, or security checks.

## Generate project-state views

`project_state.py` derives non-normative status views from existing project-owned sources. It never updates the project's root `STATUS.md` or `TODO.md`.

For a The Note layout:

```bash
python "$SCRIPTS/project_state.py" \
  --root /path/to/The-Note \
  --adapter the-note \
  --out /tmp/architecture-governance \
  --write
```

To compare existing generated files with a fresh projection:

```bash
python "$SCRIPTS/project_state.py" \
  --root /path/to/The-Note \
  --adapter the-note \
  --out /tmp/architecture-governance \
  --check
```

Outputs:

- `project-state.json` — normalized projection and provenance
- `STATUS.generated.md` — declared readiness and observed execution status
- `TODO.generated.md` — imported open issues/work and verification gaps

The adapter reads the target's `docs/architecture.toml`, `docs/quality/probes.toml`, `docs/quality/readiness.toml`, and Rust probe markers. For other layouts, export a normalized JSON snapshot from the project's **existing** registries and pass it with `--input`.

Optional `--issues` imports target-owned `[[issue]]` and `[[work]]` TOML records; `--evidence-dir` reads compatible execution records. Neither option creates a second authoritative registry.

**Limit:** A probe marker is merely a location hint. A labeled command success is not proof that a probe's assertions cover its contract. The compiler deliberately does **not** certify semantic readiness. Generated status must not replace manually owned root documents without a reconciled migration and appropriate freshness checks.

[Exchange format](../plugin/skills/architecture-governance/references/project-state-format.md) · [Migration workflow](../plugin/skills/architecture-governance/workflows/project-governance.md)

## Inspect candidate change impact

`impact.py` traverses reverse dependencies declared by semantic owners and lists related contracts, probes, and source-marker locations.

```bash
python "$SCRIPTS/impact.py" \
  --root /path/to/The-Note \
  --adapter the-note \
  --owner core-runtime
```

The owner ID must exist in the target registry. You can repeat `--owner`. Other projects can use `--input` with an exported normalized snapshot.

**Limit:** Missing graph edges and runtime relationships may leave out real consequences. Treat the output as a review starting point, not an exhaustive affected-test selector.

## Enforcement belongs to the target project

These helpers do not automatically block file writes, verify the semantics of a specification, or apply branch protection. The target project's CI should run its own architecture lint, native tests, and required conformance probes.

For work on this plugin itself, see [CONTRIBUTING.md](../CONTRIBUTING.md).
