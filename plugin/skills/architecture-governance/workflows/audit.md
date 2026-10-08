# Audit/review: try to falsify the architecture

Audit **normative documents against each other** as well as implementation against the owning contracts. Read `references/system.md`, `references/decisions.md`, `references/evidence.md`; for document audits also `references/writing.md`.

## Procedure

1. Establish the source hierarchy (normative owners, dependencies, implementation, status/roadmap, generated views). Do not let implementation or status reports override the owner.
2. Enumerate relevant invariants and their scope. For each, locate actual producers/consumers and externally observable effects, including reconfiguration, crash, cancellation, replay and unauthorized callers where applicable.
3. Search for concrete counterexamples: two sources of truth; order- or timing-dependent outcomes; component/schema mismatch; invalid state transitions; stale result mutating new authority; cache becoming durable; hidden fallback; direct cross-boundary shortcut; security declared but not enforced by the OS.
4. Check **self-consistency of the specifications**: same concept with incompatible definitions, missing lifecycle/failure dispositions, unclosed choice disguised as MUST, requirements unsupported by a designated verification owner, circular normative ownership.
5. Check the *validator itself*: is its asserted proof scope broader than what its implementation checks? For a proposed diff, check affected paths and negative probes. A passing linter is not proof of all semantics.
6. Produce a finding for each issue:
   - ID / severity / confidence (CONFIRMED, PROBABLE, NEEDS_RUNTIME_EVIDENCE)
   - normative rule and owner with exact path/location
   - actual code/doc evidence
   - minimal counterexample or forbidden state
   - impact and smallest owner-correct repair
   - falsification/verification plan
7. Separate a genuinely unimplemented future contract from present noncompliance. Record missing evidence as UNKNOWN, not an implementation failure.

Never call a speculative naming pattern a confirmed duplicate authority. Prove identity of the *responsibility*, not similarity of filenames. If you cannot read the relevant files or run a needed probe, report the limit.

**Output:** prioritized findings with causal evidence and targeted corrections, plus areas checked without detected violation. Do not imply that uninspected code passed.
