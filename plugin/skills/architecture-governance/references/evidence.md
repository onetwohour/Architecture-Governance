# Evidence Rules

Load this file for probes, tests, readiness, concurrency validation, security claims, performance evidence, or completion evidence.

- **E1 MUST — Claims need proportionate enforcement/evidence.** Prefer lint, compile/bind checks, negative tests, adversarial fixtures, or runtime probes; if automation is impractical, leave an explicit review trigger and required evidence.
- **E2 MUST — Probes try to falsify spec closure, not just demonstrate success.** A reference harness should show whether implementation can follow the contract without inventing new semantics.
- **E3 MUST — Classify validation failures by layer.** Distinguish implementation defects, owner-local design defects, and specification defects; do not dump solvable engineering problems into NEEDS_DECISION.
- **E4 MUST — Critical probes include a negative path and forbidden observable state.** Define preconditions, stimulus/interleaving/crash point, expected state, and states that must never be observable.
- **E5 MUST when concurrency/interleaving affects semantics — Control interleavings explicitly.** Do not rely on thread-timing luck.
- **E6 MUST when explicit readiness states are tracked — Readiness rises only with evidence.** Labels such as DRAFT/SEMANTICALLY_CLOSED/PROBE_VALIDATED/IMPLEMENTATION_READY require the corresponding mandatory probes and result evidence.
- **E7 MUST — Counterexamples may lower readiness.** Repair the owner/probe instead of protecting a status label with exceptions.
- **E8 MUST — A bypass cannot make a probe pass.** Test-only branches, raw mutation, special host paths, or parallel authorities that bypass the invariant invalidate PASS.
- **E9 MUST for whole-corpus closure validators — Enumerate the full violation set.** Do not stop at the first error; PASS only when the set is empty.
- **E10 MUST when generated indexes/inventories exist — Generated inventories aid navigation; they do not own truth.**
- **E11 MUST when security/isolation/capability guarantees are claimed — Test actual enforcement adversarially.** Attempt bypass, authority widening, and stale-authority use.
- **E12 SHOULD when performance is architectural — Track structural metrics as well as wall-clock time.** Examples: allocations, bytes copied, node count, invalidation/reuse, queue depth.
- **E13 MUST when plans use phase/stage/readiness gates — Behavior proves the stage, not the existence of structs/modules/docs.** For shared/runtime abstractions, implementation-ready claims normally require a vertical slice plus a second materially different case/provider/substrate, not only the first successful implementation.
- **E14 MUST — Probe harnesses stay minimal and non-authoritative.** A conformance harness must not become a replacement product path or second authority.
- **E15 MUST for validators, linters, and generated audits — State the proof boundary.** Report what the check proves and what it does not prove. Structural closure, file coverage, schema validity, and passing fixtures must not be presented as semantic correctness beyond the evidence actually checked.
