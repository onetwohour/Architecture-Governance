# Decision Rules

Load this file when the task asks "which approach?", when requirements are ambiguous, or before escalating an engineering question into a product decision.

- **J1 MUST — Classify ambiguity first.** Distinguish specified architecture, implementation freedom, local/spec defect, and genuinely unspecified product policy. Only the last category requires a product decision.
- **J2 MUST — Keep the product-decision threshold high.** Inspect owners, dependencies, and canonical extension points first. Escalate only when invariants cannot rank the options, all options satisfy correctness/security/determinism/extensibility, and a real user-experience tradeoff remains.
- **J3 MUST — Difficulty is not product policy.** New types/fields, large refactors, many changed files, or retiring an internal API do not by themselves justify a product decision.
- **J4 MUST — Architecture change means semantic-law change.** Classify by changes to system-wide closed laws, dependency direction, durable truth ownership, public-contract defaults, or identity/ordering/authority/failure law—not diff size.
- **J5 MUST — Missing documentation does not prove architecture change.** First test whether the requirement fits an existing extension point or contract extension.
- **J6 MUST — Fix local design defects at the owner.** If closed laws need not change, redesign the narrow/broken owner instead of adding a lower-layer workaround.
- **J7 MUST — Architecture-defect claims carry proof.** Identify the current owner, attempted extension points, exact expressiveness failure, violated invariant, why implementation/contract extension is insufficient, the minimum law change, and a minimal counterexample.
- **J8 MUST — Use a deterministic default order.** Prefer stronger invariant preservation, canonical-owner reuse, more general/composable abstractions, derived state over new truth, pre-validation over runtime fallback, and explicit identity/order/failure over implicit behavior.
- **J9 MUST — Settings are not correctness escape hatches.** Do not turn correct/incorrect, safe/unsafe, deterministic/order-dependent, or canonical/bypass behavior into a user setting. Every offered option must satisfy core invariants.
- **J10 MUST — Current code is not architecture authority.** Repeated workarounds do not become intended architecture by repetition; determine whether they are implementation violations or owner defects.
- **J11 MUST — Spec defects are normal self-correction signals.** When implementation finds a counterexample, repair the owner and probe instead of preserving a bad abstraction.
