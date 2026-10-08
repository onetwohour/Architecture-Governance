# Implement: preserve the law and audit the diff

Use `workflows/plan.md` first, scaled to change risk. For architecture-relevant code read `references/system.md`, `references/decisions.md` and `references/delivery.md`. For new normative prose also read `references/writing.md`.

1. **Before edits:** identify the owner and normative dependencies; inspect the actual existing primitive before adding any registry, store, manager, adapter, scheduler, cache or fallback. Write a minimal scope/validation plan.
2. **During edits:** apply the change at the canonical owner, maintain public representations consistently, and add the smallest meaningful *negative* probe or conformance case. Keep derived views derived. Do not modify generated reports as if they were sources.
3. **If unexpected meaning emerges:** stop extending the implementation on that assumption. Identify the counterexample, classify the defect and correct the normative owner/contract first; then adapt the code and probes. For changes to system-wide laws, make the new invariant and dependent owners explicit.
4. **After edits:** inspect `git diff`, staged changes and untracked additions. Look for unplanned paths, direct dependency bypasses, extra mutation authorities, new defaults/timeouts, stale callbacks, cancellation mistaken for commit, and tests that avoid production paths.
5. **Execute evidence:** use the project's actual lint/build/tests/architecture probes for the affected area. Prefer adversarial assertions about forbidden states over positive-only checks. Run broader regression checks when affected-test selection is uncertain.
6. **Close honestly:** report exact commands/results and any UNKNOWN or STALE evidence. A successful build is not contract readiness.

`change_scope.py` can highlight unplanned files from a temporary plan; it cannot find semantic duplication or prove the completeness of planned paths. A plan may be revised with reasons, but never silently rewritten after a violation to manufacture PASS.

For local isolated changes, limit steps to owner check, targeted code/test change, diff review and test. Do not manufacture architecture records.
