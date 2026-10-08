# Architecture Governance

**English** · [한국어](README.ko.md)

A Claude Code plugin with **one architecture-governance skill** for planning, implementing, auditing, reviewing and verifying software changes. It is designed to make architecture requirements actionable without replacing your project's own contracts.

The skill is not an architecture framework or a claim that an agent can prove every invariant. Its work is to find the authoritative owner, reason about observable behavior, challenge proposed changes and report exactly which checks ran.

## Install

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

Restart your Claude Code session after installation. The canonical distribution is the `plugin/` directory in this repository, through the plugin marketplace above.

## Use

The command is `/architecture-governance:architecture-governance` when invoked via the plugin; the short alias may also be available depending on installed skills.

| Mode | Example | Result |
| --- | --- | --- |
| `plan` | `/architecture-governance:architecture-governance plan redesign the checkpoint recovery path` | Owner/contract analysis and scope proposal |
| `implement` | `... implement fix stale editor responses` | Owner-first change, diff audit and targeted checks |
| `audit` | `... audit normative docs and implementation` | Falsifiable, source-linked findings |
| `review` | `... review my current git diff` | Semantic diff assessment and proof gaps |
| `verify` | `... verify the persistence probes` | Actual test/evidence summary |
| `project` | Compile derived status/TODO from existing source registries |
| `adopt` | `... adopt this in my project` | Local integration guidance without duplicate authorities |

Modes are arguments to **one** Skill, not six separate Skills. Without a mode it defaults to planning, unless the request clearly indicates another task.

## How it works

1. Read the target project's normative owner and dependencies; don't mistake current code or status reports for authority.
2. Classify risk by semantic impact (local implementation, owner-local contract, system-wide law).
3. Reuse the canonical owner before creating a second store, manager, adapter or mutable truth.
4. Make an explicit plan for affected paths, contracts, forbidden states and tests.
5. Examine the actual diff and try negative/failure cases before claiming completion.
6. Report PASS, FAIL, UNKNOWN, STALE or REVIEW_REQUIRED with evidence and limits.

Five **workflow files** make these steps operational, while five existing **rule references** retain the 101 rules for ownership, runtime semantics, decision-making, specification writing and evidence. On-demand loading keeps routine work small.

## Project-state governance (v3)

The `project` mode guides a **lossless migration** from manually maintained STATUS/TODO to derived, non-normative views. It does not impose a new project database. Run the opt-in compiler against the target project's **existing sources**:

```bash
python plugin/skills/architecture-governance/scripts/project_state.py --root /path/to/The-Note --adapter the-note --out /tmp/governance-output --write
python plugin/skills/architecture-governance/scripts/project_state.py --root /path/to/The-Note --adapter the-note --out /tmp/governance-output --check
python plugin/skills/architecture-governance/scripts/impact.py --root /path/to/The-Note --adapter the-note --owner core-runtime
```

The Note adapter reads `docs/architecture.toml`, `docs/quality/probes.toml`, `docs/quality/readiness.toml` and Rust probe markers. It does not edit the project or assert that marker presence means passing tests. Other projects supply an **exported normalized JSON** through `--input`, not a second manually maintained source. See [project governance workflow](plugin/skills/architecture-governance/workflows/project-governance.md) and [exchange format](plugin/skills/architecture-governance/references/project-state-format.md).

Optional target-owned `[[issue]]` and `[[work]]` records preserve the distinction between problems and planned tasks; Work dependency cycles are rejected. An Issue already assigned to open work is not duplicated in the generated TODO.

The outputs are `project-state.json`, `STATUS.generated.md` and `TODO.generated.md` in the explicitly chosen directory. They are **projections**, not replacements for root STATUS/TODO until an audited migration is complete. Probe commands may be associated with evidence records via `--evidence-dir`, but COMMAND_PASS indicates only individual command success, never verified Probe coverage or semantic readiness. Reverse dependency impact results are **candidates**, not a sound/complete affected-test set.

[Policy tension review](doctrine/POLICY_REVIEW.md) highlights possible conflicting interpretations of the existing 101 rules and the remaining manual evaluation requirements.

## Optional executable helpers

Python 3.10+ and Git; no third-party Python dependencies. These tools **do not run automatically**, install hooks, edit source code, or declare an architecture correct.

**Read-only scope audit:**

```bash
python plugin/skills/architecture-governance/scripts/change_scope.py \
  --repo /path/to/project --plan /tmp/change-scope.json --base HEAD
```

The plan is a temporary JSON object with `allowed_paths` and optionally `protected_paths` glob arrays. See [example](plugin/skills/architecture-governance/templates/change-scope.json). The audit includes tracked/staged/unstaged changes and nonignored untracked paths. Exit 0 = within declared paths; 1 = protected path changed; 2 = unplanned paths need review; 3 = tool error. Path checks are **not** semantic design checks.

**Run one actual validation command and capture evidence:**

```bash
python plugin/skills/architecture-governance/scripts/run_validation.py \
  --repo /path/to/project --label unit-test --output /tmp/unit-evidence.json \
  -- python -m unittest discover -s tests
```

Command arguments run **without a shell**. The JSON records exit status, platform, Git revision, dirty worktree status and bounded output. A green command is evidence only for its own assertions; a dirty-worktree pass is not a reusable clean-commit certificate. The helper does not replace CI, security probes, or architecture review.

## Agent behavior evaluation

[Adversarial scenarios](evaluations/adversarial-cases.md) define manual checks for duplicate authority, silent fallbacks, stale evidence, scope laundering and proportionate handling of small edits. Script tests cannot substitute for these model behavior evaluations.

## Limits and adoption

A Skill cannot enforce itself if not invoked, cannot guarantee that every modification passes through a hook, and cannot certify semantic ownership from file names. Connect your project's native architecture gates and adversarial tests to its **own CI/branch protection**. Do not duplicate its owner registry, probes, readiness facts or issue tracker inside this plugin.

See [adoption workflow](plugin/skills/architecture-governance/workflows/adopt.md) and [Engineering Constitution](doctrine/ENGINEERING_CONSTITUTION.md).

## Validate this repository

```bash
python plugin/skills/architecture-governance/scripts/validate.py
python tests/validate_repository.py
python -m unittest discover -s tests -p 'test_*.py' -v
python -m compileall -q plugin/skills/architecture-governance/scripts tests
```

These tests check plugin structure, rule inventory and helper behavior. They do **not** establish target-project architecture correctness.

## License

[Apache-2.0](LICENSE)
