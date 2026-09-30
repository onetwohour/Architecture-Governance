# System Rules

Load this file only for architecture, runtime, ownership, state, persistence, or security work.

## Ownership

- **O1 MUST — Single authority.** One normative owner defines each semantic responsibility. Other documents/components reference or derive from it; conflicts are ownership/spec defects, not precedence problems.
- **O2 MUST if the architecture has multiple semantic owners — Owner graph.** Treat architecture as a graph of semantic owners and dependencies; top-level docs map the graph instead of redefining its details.
- **O3 MUST — Reuse before create.** Before adding a manager, registry, store, dispatcher, service, UI primitive, or persistence representation, find the existing owner. If it is too narrow, generalize or redesign it instead of adding a parallel layer.
- **O4 MUST — No parallel authority.** Do not add a second path that decides the same meaning. Temporary adapters/bridges are justified only when they connect genuinely different contracts; owner-adjacent patch budget defaults to zero.
- **O5 SHOULD — Prefer change locality.** A semantic change should mostly stay inside the boundary that owns it. If unrelated layers require coordinated edits, re-check the boundary.
- **O6 MUST when independent replacement/removal matters — Contract-mediated coupling.** Components depend on public semantic contracts, not each other's internals.
- **O7 MUST when optional modules/features are claimed — Minimal configuration conforms.** The smallest/empty composition must still have a valid lifecycle.
- **O8 MUST for extension/plugin ecosystems — Open extensions, closed laws.** Separate extensible surfaces from system-wide laws such as identity, ordering, authority, commit, and failure.
- **O9 MUST when a standard extension path and escape hatch coexist — Extend before escape.** Improve the canonical extension surface before routing ordinary features through a bypass.
- **O10 MUST when extensibility/modularity is claimed — Add/remove/replace/compose.** Extensibility means all four, not merely adding features.
- **O11 SHOULD unless subsystems truly have independent deploy/security/lifetime/data boundaries — Prefer composable primitives.** Do not create a global subsystem per feature when common semantic primitives can express the behavior.
- **O12 MUST — Physical boundaries need real independence.** Create crates/packages/services for independent consumers, public APIs, security/unsafe isolation, heavy dependency isolation, or process/deploy boundaries—not merely because a concept is large. Avoid responsibility-free common/shared/utils/misc buckets.

## Abstraction

- **A1 MUST — Require independent evidence.** Promote a shared abstraction only when two independent consumers/cases use the same contract without bypasses, or when it implements a genuine closed-domain law.

## Runtime semantics

- **S1 MUST — Make dependencies and ordering explicit.** Never let registration/source/container order, thread completion, callback timing, or hidden mutable wiring determine semantics.
- **S2 MUST when access/dependencies/capabilities are declared ahead of time — Declared access equals runtime access.** Runtime must not silently widen the declared graph or authority.
- **S3 MUST when state has multiple representations/replicas — Separate authority from projections.** In centralized models, keep one semantic truth plus rebuildable projections/caches/indexes. In distributed models, explicitly define replica identity, merge/conflict law, and causal authority.
- **S4 MUST — Close the semantic matrix.** For important contracts, resolve every applicable dimension: identity, ownership, state, transition, authority, ordering, visibility/atomicity, failure, cancellation, retry/idempotency, replay, persistence, reconfiguration, concurrency, unknown/opaque handling, observability. Mark only genuine non-applicability as N/A.
- **S5 MUST when structural validation is possible — Reject knowable defects early.** Missing/ambiguous dependencies, illegal scope, incompatible schema, and similar deterministic defects should fail at compile/bind/validation rather than hide behind runtime first-match, fallback, or retry.
- **S6 MUST when observable transaction/publish/durable boundaries exist — Explicit commit boundaries.** Do not conflate commits with different semantics.
- **S7 MUST when async/external results can affect authoritative state — Canonical ingress.** Callbacks/workers/providers return through the owner's ingress/result/transaction boundary instead of mutating authoritative state directly.
- **S8 MUST for remote operations or external effects — Local cancellation is not an external terminal.** If the external outcome is unknown, represent it as indeterminate/unknown.
- **S9 MUST for replay/recovery/event sourcing — Replay recorded semantic evidence.** Reproduce recorded inputs/decisions/generation evidence; do not re-run already published external effects or guess a nearby state when evidence mismatches.
- **S10 MUST when incremental behavior is an architectural requirement — Incremental by construction.** Model change units, dependencies, invalidation, and reuse from the start rather than bolting optimization onto full recomputation.
- **S11 MUST when versioning/opaque extensions/partial knowledge exist — Preserve unknowns.** Do not map unknown schema/variant/owner/evidence to guessed defaults or nearest known cases; define preservation and forbidden operations.
- **S12 MUST — Performance does not justify semantic bypass.** Optimize within canonical ownership, authority, commit, isolation, and validation boundaries.
- **S13 MUST when multiple authoring/front-end/API surfaces produce the same system — Lower to one model.** Convenience surfaces compile/lower into the same canonical declarations/contracts instead of creating a second semantic runtime.
- **S14 MUST when physical execution can restart or multiply — Separate semantic and execution identity.** Process/thread/connection/handle identity is not logical operation/object/principal/generation identity.
- **S15 MUST when restart/reconfiguration/provider replacement exists — Names do not prove identity or state carry.** Define identity and carry explicitly.
- **S16 MUST when topology is fixed during compile/bind — Freeze topology.** Running code must not re-open manifest/catalog/name lookup to add hidden wiring; topology changes require an explicit reconfiguration contract.

## Data and security

- **T1 SHOULD when users own durable portable content — User data outlives product metadata.** Preserve generally representable user content even if product-specific metadata or the product disappears.
- **T2 MUST for shared/external/multi-writer artifacts — Conflict-aware writes.** Compare expected identity/revision/digest with current state and surface conflicts instead of silently overwriting another writer.
- **X1 MUST when claiming sandbox/isolation/trust tiers — Security terminology matches enforcement.** Never describe in-process/native execution as sandboxed or isolated unless the actual authority boundary enforces that claim.
