# Contributing to Architecture Governance

This document is for people maintaining the plugin, its policies, scripts, and tests. For installation and everyday use, start with the [README](README.md). For optional CLI helpers, see [docs/TOOLS.md](docs/TOOLS.md).

## Repository layout

| Path | Purpose |
| --- | --- |
| `plugin/skills/architecture-governance/SKILL.md` | Skill entry point and mode routing |
| `plugin/skills/architecture-governance/workflows/` | Task-specific procedures |
| `plugin/skills/architecture-governance/references/` | Active engineering rules and tool formats |
| `plugin/skills/architecture-governance/scripts/` | Optional deterministic helper programs |
| `plugin/skills/architecture-governance/templates/` | Example outputs and temporary plans |
| `doctrine/` | Human-readable policy index and non-normative policy review |
| `evaluations/` | Adversarial agent-behavior evaluation cases |
| `tests/` | Executable tests for repository structure and helper behavior |
| `.github/workflows/validate.yml` | CI checks for this repository |

The Skill defines **method**, not the architecture of any target project. Do not copy target-specific contracts, owner registries, test results, or issue records into plugin policy.

## Development environment

- Python **3.11+**
- Git
- No third-party Python dependencies

Run repository checks from the repository root:

```bash
python plugin/skills/architecture-governance/scripts/validate.py
python tests/validate_repository.py
python -m unittest discover -s tests -p 'test_*.py' -v
python -m compileall -q plugin/skills/architecture-governance/scripts tests
```

GitHub Actions runs these same categories of checks on push and pull request. Their successful completion proves the checks in this repository passed, **not** that an agent obeyed the skill on real software or that a target architecture is correct.

## When changing the skill

1. Keep `SKILL.md` focused on entry-point behavior, routing, and invariant method. Place longer procedures in the relevant workflow or reference.
2. Prefer clarifying or correcting the existing rule that owns a concern over introducing a duplicate rule.
3. Maintain the active-rule inventory across the five references indexed by [Engineering Constitution](doctrine/ENGINEERING_CONSTITUTION.md). The repository validator currently checks the expected 101 rule IDs and other structural constraints; passing it is not a semantic consistency proof.
4. Update workflows when a rule changes how an agent should investigate, implement, or verify. Do not leave policy without an actionable route.
5. Add negative tests for helper regressions and distinguish tool behavior from agent behavior.
6. Keep the public READMEs focused on installation, use, benefits, and limits. Keep implementation details here, and command-line specifics in [docs/TOOLS.md](docs/TOOLS.md).

Use [POLICY_REVIEW.md](doctrine/POLICY_REVIEW.md) to track possible interactions among rules. It is non-normative and must not quietly become another active policy source.

## When changing a helper

- Preserve the distinction between structural checks, command execution, and semantic verification.
- Treat records supplied by callers or untrusted directories as claims, not automatically authenticated evidence.
- Prefer deterministic, read-only behavior. Writing generated reports must require an explicit action and must never silently replace authoritative target files.
- Test failures, stale state, unresolved references, unexpected changes, and unsupported inputs as well as success.
- Keep version/runtime requirements and CLI examples accurate in [docs/TOOLS.md](docs/TOOLS.md).

## Evaluating real agent behavior

The helper tests do **not** establish that Claude will preserve a target's architecture. Use the cases in [evaluations/adversarial-cases.md](evaluations/adversarial-cases.md) against disposable representative repositories.

Record the target revision, exact request, whether the skill was invoked, observed plan, actual diff, executed checks, and an independent PASS/FAIL/NOT_RUN assessment. Examine both failure to reject violations and overreaction to harmless isolated edits.

Changes to the entry point or workflows should be evaluated for actual agent behavior before claiming improved compliance. The presence of adversarial scenarios alone is not an evaluation result.

## Documentation boundaries

- **README / README.ko.md:** What the plugin does, how to install and use it, and what it cannot guarantee.
- **docs/TOOLS.md:** Optional command-line tools, input/output contracts, and execution limits.
- **CONTRIBUTING.md:** Repository layout, policy maintenance, testing, and agent evaluation.
- **Skill workflows and references:** Instructions consumed by the agent, not duplicate user manuals or development history.

Release history belongs in Git history or a dedicated changelog, not in introductory README sections.
