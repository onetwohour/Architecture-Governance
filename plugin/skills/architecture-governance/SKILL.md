---
name: architecture-governance
description: Architecture-first engineering for non-trivial code or specification changes. Use for subsystem design, implementation planning, refactors, architecture audits, contract changes, concurrency, persistence, plugin boundaries, and evidence-based verification. Detect duplicate authority, hidden ordering, spec gaps, uncontrolled change scope, and unproven completion. Skip truly isolated edits without semantic impact.
argument-hint: "[plan|implement|audit|review|verify|adopt] [task or target]"
---

# Architecture Governance

You are working **within the target project's architecture**, not installing a universal architecture. This skill governs the *method*; the target's normative owners govern the *meaning*. Its scripts are read-only inspection or explicit test runners, not semantic judges.

## Arguments and routing

Read `$ARGUMENTS`. The first word selects a mode; absent or unrecognized mode defaults to **plan**, treating all arguments as the task. If the user's intent clearly requests another mode, use it. Load the corresponding workflow:

| Mode | Read | Purpose |
| --- | --- | --- |
| `plan` | `workflows/plan.md` | Discover owners, contracts, risks and tests before changing code |
| `implement` | `workflows/implement.md` | Plan, change, diff-audit, verify |
| `audit` | `workflows/audit.md` | Audit architecture, including the normative documents themselves |
| `review` | `workflows/audit.md` | Compare a proposed diff with its owners and failure cases |
| `verify` | `workflows/verify.md` | Run and characterize actual evidence |
| `adopt` | `workflows/adopt.md` | Integrate the skill with a project without duplicating its authority |

If the task is a trivial isolated edit, use a lightweight version of the loop. Do not demand heavyweight architecture artifacts merely because this skill was invoked.

## Non-negotiable method

1. **Locate the authority.** Inspect repository instructions, owner/contract registries where present, normative documents and their declared dependencies. Do not infer intended architecture from STATUS/TODO, old code, or this skill.
2. **Understand before extending.** Trace actual producers, consumers, state mutation paths, identity, lifecycle, persistence, failures and existing extension points relevant to the change. Prefer repairing the existing owner to a second manager/store/registry or a compatibility patch.
3. **Classify the work.** Distinguish local implementation choice, owner-local contract defect, system-wide law change and an unresolved product-policy decision. Diff size alone is not architecture impact.
4. **Make a risk-proportionate plan.** Identify expected paths, owner/contract impact, forbidden states, affected probes and verification commands. Escalate if implementation discovers new semantics or crosses an unplanned authority boundary.
5. **Challenge the result.** Verify negative/failure paths, cancellation vs. external completion, stale generation, ordering, retry and replay where relevant. Inspect the *actual* diff, not only the intended edits.
6. **Separate claims.** Source exists ≠ test implemented ≠ test executed ≠ invariant proven. Present PASS, FAIL, UNKNOWN, STALE, or REVIEW_REQUIRED with evidence and its limits. Never upgrade unknown to pass.

When a specification cannot determine externally observable behavior, report the precise gap and repair the responsible normative owner before depending on a guessed default. Never hide design defects behind fallbacks, timeouts, special host paths or test-only bypasses.

## On-demand rule books

These five files contain the **101 existing active engineering rules**; load only the relevant set. They are guidance *subordinate* to the target project's normative contracts.

- `references/system.md` — ownership, runtime, persistence, concurrency and security
- `references/decisions.md` — decision classification, alternatives and escalation
- `references/writing.md` — self-contained specifications and precise language
- `references/evidence.md` — falsification, readiness and proof boundaries
- `references/delivery.md` — implementation workflow and completion

Read `references/system.md` plus `references/decisions.md` for architectural changes; `references/evidence.md` for every verification or readiness claim. Templates under `templates/` are optional forms, not new owners.

## Executable helpers (opt-in)

- `python scripts/change_scope.py --repo <path> --plan <json> [--base HEAD]` compares changed paths against an explicit *temporary* scope plan. Unexpected changes require review, not automatic condemnation.
- `python scripts/run_validation.py --repo <path> --label <id> --output <path> -- <argv...>` executes **one real command** without a shell and records evidence. It does not prove semantic correctness beyond that command.

Use repository-native build, lint, probe, conformance and CI commands when available. Never replace them with this skill's helpers. Do not install hooks or block project writes silently. Persistent enforcement belongs in the target project's own CI and policies.

## Finish

Give a compact, traceable report: owner and invariant; reused/changed abstractions; affected files/contracts; actual checks and results (commands, revision/worktree state); unverified/negative paths; outstanding blockers. If a requested change cannot be safely completed, report the exact boundary, not a fabricated success.
