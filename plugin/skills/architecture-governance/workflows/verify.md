# Verify: evidence is not a narrative claim

Read `references/evidence.md` and the target project's probe/test definitions. The governing invariant comes from the target project's normative owner; the test's own assertions are not its source of truth.

## Required distinctions

- **DEFINED**: a probe/requirement is registered.
- **LOCATED**: test or marker exists; it may not be runnable.
- **EXECUTED**: a specific command actually ran, with exit status, revision, environment and output.
- **PROVEN WITHIN SCOPE**: the executed assertions are relevant to an invariant and its forbidden state. This requires inspection, not only exit code.
- **READY**: all required contract-specific proof gates are satisfied. One green unit test never implies this automatically.

## Workflow

1. Resolve affected owner/contracts and the necessary positive, negative, concurrency and recovery scenarios.
2. Discover actual test targets and runner commands. Do not assume a comment marker is executable.
3. Run each check via existing project commands, or `scripts/run_validation.py` to capture its exit/result and revision in JSON. The helper uses argument arrays without a shell and executes only a command explicitly supplied by the operator.
4. Distinguish PASS, FAIL, UNKNOWN, STALE and REVIEW_REQUIRED. A previous revision's pass cannot be silently carried forward. A dirty worktree run is evidence of that **working tree**, not a reusable certificate for a clean commit.
5. Inspect what the assertions prove and what they do **not** prove. For high-risk ownership/security claims attempt bypasses and negative paths against the real boundary.
6. State platform gaps, unrun checks, partial coverage and failures. Do not report overall READY unless the project's readiness policy is satisfied.

To navigate a project's declared contracts, `scripts/project_state.py` can build a read-only projection from authoritative sources and evidence. Its `semantic_readiness` is always NOT_ASSESSED; review the real assertions and project readiness policy independently.

The evidence collector stores exit status, command, time, platform, Git revision and dirty flag. It intentionally makes **no semantic-readiness claim**. Never use the helper to replace full native test suites or a required CI job.
