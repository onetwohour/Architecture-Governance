---
name: architecture-governance
description: Design, review, refactor, or normalize non-trivial software architecture and specifications using semantic ownership, explicit contracts, stable documentation rules, evidence-backed probes, and completion gates. Use for architecture design/review, specification cleanup, large refactors, implementation-vs-design audits, structural defect analysis, ADR/contract normalization, reusable engineering rules, or changes that risk parallel managers/stores/dispatchers/bridges or hidden semantic ordering. Do not use for trivial isolated edits with no architectural or contract impact.
---

# Architecture Governance

Apply this workflow to the target project. Preserve the target project's domain; do not import product-specific topology from the methodology.

## Policy authority

- `references/rule-registry.json` is the single canonical rule registry.
- `references/engineering-constitution.md` is the complete readable projection of that registry.
- Other reference documents are focused projections and must not invent conflicting rules.
- Templates are output scaffolds, not policy owners.
- CORE rules are engineering invariants, not style preferences. CONDITIONAL rules apply only when their applicability condition is supported. PROFILE rules are configurable conventions.

## Required workflow

1. **Inventory evidence.** Separate normative specification, implementation status, roadmap, research, examples, generated indexes, tests, and code. Current code is evidence of implementation, not automatic architecture authority.
2. **Find semantic ownership.** Identify semantic owner, truth/authority owner, dependencies, producers, consumers, lifecycle, failure/cancellation/retry, persistence/recovery, concurrency, and extension points relevant to the task. Search by responsibility, not only by names.
3. **Classify ambiguity before asking.** Read `references/decision-policy.md`. Distinguish specified architecture, implementation freedom, local/spec defect, and genuinely unspecified product policy. Refactor size, implementation difficulty, missing primitives, or multiple internal approaches do not by themselves require a product decision.
4. **Reuse before create.** Prefer an existing owner or owner-local redesign over a new feature-local Manager/Coordinator/Registry/Dispatcher/Store/Bridge/Adapter. A new indirection carries the burden of proof.
5. **Close the contract.** For an important semantic contract, resolve every applicable dimension: identity, ownership, state, transition, authority, ordering, visibility/atomicity, failure, cancellation, retry/idempotency, replay, persistence, reconfiguration, concurrency, unknown/opaque handling, and observability. Mark genuinely inapplicable dimensions `N/A`; do not leave meaningful gaps implicit.
6. **Make semantic edges explicit.** Do not hide correctness-relevant dependency or ordering in registration order, source order, container iteration, callback timing, thread scheduling, name lookup, or ad-hoc mutable wiring.
7. **Keep references stable.** Use a document path plus a stable concept/rule ID for semantic references. Do not use positional anchors such as `§12`, `3장 2절`, or equivalent numbering as cross-document semantic references.
8. **Separate kinds of truth.** Normative architecture, implementation status, roadmap, research, and work protocol have different owners. Do not rewrite one into another.
9. **Turn critical invariants into evidence.** Important probes include a negative path and a forbidden observable state. Readiness or stage completion requires evidence, not the mere existence of modules, types, or documents.
10. **Audit completion.** Use `references/completion-gates.md` and `references/anti-patterns.md`. Known architecture violations cannot be closed as “temporary” without being explicitly left open.

## Strong defaults

- One semantic responsibility has one normative authority.
- Reuse Before Create; no parallel authority; patch budget defaults to zero.
- Extend Before Escape when a standard extension surface is incomplete.
- Shared abstractions require independent evidence: normally a second consumer/situation or a real closed-domain law.
- Change locality is a robustness signal. If one semantic change propagates through unrelated layers, re-check the boundary.
- Performance does not justify semantic bypass.
- Unknown or opaque states are preserved rather than guessed when guessing would invent semantics.
- Current implementation practice is evidence about implementation, not proof of intended architecture.

## Conditional rules

Apply a CONDITIONAL rule only when its `applies_when` condition is supported by project evidence. If it materially affects the design, state why it applies. If its exception matters, state that too.

## Output expectations

For architecture-changing work, make the result traceable enough to answer:

- semantic owner and truth/authority owner;
- existing abstraction reused or redesigned;
- new or changed contract;
- explicit dependency and ordering representation;
- durable / working / derived state impact;
- commit, side-effect, and ingress boundaries;
- failure / cancellation / retry behavior;
- replay / nondeterminism impact;
- concurrency / stale / late-result handling;
- readiness before/after and evidence;
- probe/test/gate changes;
- second-case evidence for shared abstractions;
- remaining in-scope specification defects.

Use `templates/architecture-review.md`, `templates/contract.md`, `templates/decision-record.md`, and `templates/probe.md` when they fit. Do not force a template when a compact answer is more useful.

## Reading map

- Full policy and rationale → `references/engineering-constitution.md`
- Exact rule metadata, applicability, strength, and enforcement → `references/rule-registry.json`
- Decision or “which approach?” ambiguity → `references/decision-policy.md`
- Final audit → `references/completion-gates.md` and `references/anti-patterns.md`
- Registry semantics → `references/rule-model.md`

When this skill package itself is modified, run `python scripts/validate.py` from the skill directory.
