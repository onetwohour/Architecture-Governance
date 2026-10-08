# Policy review — Architecture Governance v3

> **NON-NORMATIVE REVIEW.** This is an analysis of potential rule interactions, not a competing ruleset, a claim of exhaustively proven consistency, or an automatic semantic certification. The existing five references remain the sole active policy surface.

## What the previous validation actually proved

The former rule-set validator established only **101 distinct compact IDs** and expected file structure. That is useful but insufficient. A rule can be internally ambiguous, too general for a domain, untestable, or in tension with another rule even when its ID is unique.

The v3 review looked at the rule families, their MUST conditions and the most likely conflicting interpretations. The following tensions must be handled *explicitly* by the skill. They are not necessarily genuine contradictions.

| Rule interaction | Risky interpretation | Resolution expected from agent |
| --- | --- | --- |
| O1/O4 single authority vs S3 replicated/projection state | "One truth means one physical copy" | One semantic mutation authority may have multiple derived replicas; a distributed model must specify merge/conflict/causal law. |
| O3 reuse vs A1 independent abstraction evidence | "Reuse forces every concept into one global owner" | Reuse canonical responsibilities; shared abstraction promotion needs separate evidence or a genuinely closed law. |
| S1 explicit ordering vs concurrency optimization S12 | "Any parallel execution violates determinism" | Concurrency is allowed when the observed order/equivalence and commit laws are explicit and enforced. |
| S11 unknown preservation vs X1/X2 security | "Unknown permissions should be preserved and executed" | Retain uninterpreted bytes where required, but refuse unsupported authority/operations until independently validated. |
| S8 cancellation vs S25 recovery | "Cancel implies external success/failure" | Preserve unknown external outcome and provenance; define reconciliation and idempotency. |
| E6 readiness labels vs E15 proof boundary | "A registered PASS marker proves a contract" | Differentiate declaration, location, actual execution and semantic evidence; tool PASS never certifies complete semantics. |
| D2/D9/D18/D19 status ownership | "Split STATUS into many manually edited authoritative files" | Keep open defects, work decisions and evidence in their own existing owners; generate views when useful without copying authority. |
| F1 speculative compatibility vs T1 user portability | "Pre-release means discard all existing durable data" | F1 is conditional on *absence* of external compatibility/data obligations; real data protection continues to apply. |
| D7 normative MUST vs J1 unresolved decision | "Invent policy to satisfy a template" | If owners do not close an observable policy, record the gap and correct the owner, not a runtime default. |
| W2 affected representations vs O5 change locality | "Always modify every layer" | Enumerate actual semantic representations; unnecessary coordinated edits indicate boundary problems. |

## Residual risks

- Some MUST clauses are intentionally conditional. Their precondition and observable scope must be checked, not mechanically applied to every function.
- A rule may be editorial or methodological and cannot be proven from paths or automated lint alone.
- An owner graph with missing dependency edges will produce an **under-approximation** of impact. Treat `impact.py` as a candidate list; add tests through semantic review.
- A command evidence record without trusted CI attestation may be forged. Project security gates require independently verifiable provenance where needed.
- Change Scope's glob check detects unexpected paths, not unauthorized changes to semantics within allowed paths.
- No live Claude model evaluations of the 12 adversarial cases are included in this commit. The test files only exercise deterministic helper behavior.

## Release improvements

1. Added a project-state compiler with explicit proof boundary; it does not promote imported readiness.
2. Added reverse-owner impact analysis from declared dependencies, with a visible incompleteness warning.
3. Added a project governance workflow for STATUS/TODO migration, issue ownership, evidence and generated projections.
4. Added negative tests for false readiness, stale evidence, owner/probe reference breaks and root-file overwrite attempts.

## Next quality bar

Execute the 12 cases in `evaluations/adversarial-cases.md` with the actual Claude Code skill against representative target repositories, recording prompts, diffs, tests and independent acceptance results. Only then can behavior-level gains be assessed.
