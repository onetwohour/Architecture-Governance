---
name: architecture-governance
description: Review or change non-trivial software architecture and specifications with explicit ownership, contracts, ordering, evidence, and completion criteria. Use for architecture design/review, specification cleanup, large refactors, implementation-vs-design audits, structural defects, shared abstractions, persistence/concurrency/retry semantics, or work that risks parallel authorities or hidden ordering. Skip for trivial isolated edits with no contract or architecture impact.
---

# Architecture Governance

Use the target project's own domain model. This skill supplies decision and review discipline, not product topology.

## Default loop

1. Separate normative design, implementation status, roadmap, research, tests, generated indexes, and code.
2. Identify the semantic owner, mutation authority, dependencies, producers/consumers, lifecycle, failure/retry, persistence, concurrency, and extension points that matter.
3. Reuse or redesign the existing owner before creating another manager, store, registry, dispatcher, bridge, or authority path.
4. Close every applicable contract dimension: identity/equality, ownership, state, transition, authority, ordering, visibility/atomicity, failure, cancellation, retry/idempotency, replay, persistence, reconfiguration, concurrency, unknown/opaque handling, observability.
5. Make correctness-relevant dependencies and ordering explicit; never rely on registration order, container iteration, thread timing, callback timing, or hidden mutable wiring.
6. Validate important invariants with negative cases and forbidden observable states.
7. Do not claim readiness or completion without evidence.

## Hard defaults

- One semantic responsibility has one normative authority.
- Current code is implementation evidence, not automatic architecture authority.
- Reuse before create; patch budget defaults to zero for owner-adjacent workarounds.
- Extend the canonical surface before using an escape hatch.
- Shared abstractions need independent evidence: normally a second real consumer/case or a closed domain law.
- Unknown state is preserved, not guessed.
- Fallbacks, defaults, bounds, and timeouts need an owner and a reason; providers do not invent them.
- Physical/runtime identifiers and self-asserted payloads do not become semantic or security identity.
- Performance never justifies bypassing ownership, authority, commit, isolation, or validation boundaries.
- Known in-scope architecture/spec violations are not "done" because they are labeled temporary.

## Load only what the task needs

- Architecture, runtime, ownership, state, persistence, security → `references/system.md`
- "Which approach?", ambiguity, product-vs-engineering decisions → `references/decisions.md`
- Specs, docs, comments, wording, references → `references/writing.md`
- Tests, probes, readiness, security/performance evidence → `references/evidence.md`
- Change workflow, completion, greenfield compatibility → `references/delivery.md`

## Writing

Write model-facing guidance in concise English. Match the target project's requested output language.

Do not anthropomorphize software with unmodeled intent, desire, knowledge, memory, or judgment. Name the actual state, policy, authority, observation, transition, or stored fact. Ordinary active voice is fine when it names a defined operation: "the parser rejects invalid input" is precise; "the cache knows" is not.

Use stable semantic references (path + concept/short rule ID), not positional section references such as §12 or "chapter 3, section 2".

## Output

For architecture-changing work, make the result traceable enough to identify: owner/authority, reused or redesigned abstraction, changed contracts, explicit dependency/order, state ownership, commit/effect/ingress boundaries, failure/retry behavior, replay/nondeterminism impact, concurrency/stale-result handling, evidence, and remaining in-scope defects.

Use templates only when they improve the result. Keep ordinary answers compact.
