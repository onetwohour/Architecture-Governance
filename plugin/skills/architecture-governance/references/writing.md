# Writing Rules

Load this file for specifications, architecture docs, comments, terminology, cross-references, or editorial review.

## Documentation

- **D1 MUST — Use stable semantic references.** Refer by path + stable concept/short rule ID, never by positional anchors such as §12 or "chapter 3, section 2".
- **D2 MUST — Separate normative design from status, roadmap, benchmarks, bug diaries, and research.**
- **D3 MUST — Separate architecture from work protocol.** Architecture defines what must be true and who owns the meaning; implementation guides define what to inspect, execute, and report.
- **D4 MUST — Close project-owned semantics locally.** If the project owns type/lifecycle/derivation/failure semantics, define them in the owning spec. External RFCs/standards may be declared dependencies but cannot substitute for project-owned meaning.
- **D5 MUST — Define before normative use.** Any named concept that affects execution semantics needs an owner and implementable definition before normative use. Canonical records/variants also close transitive type references to zero unresolved project-owned leaves.
- **D6 MUST — A name is not a definition.** Canonical records/variants/protocols/derivations need the fields, payloads, invariants, states, and failure rules required to implement them. Do not promote examples or smell labels into canonical concepts.
- **D7 MUST — Fix normative strength.** Use MUST/MUST NOT/SHOULD/MAY/DEFAULT/EXAMPLE consistently; vague words such as "initial", "default", or "example" do not replace normative strength.
- **D8 MUST — Rewrites must not silently weaken invariants.** Splitting, summarizing, renaming, or rewriting requires an explicit owner change and regression/counterexample evidence if semantics are weakened.
- **D9 MUST when implementation status is tracked in docs — Give status one owner.** Do not duplicate the same status across normative contracts and implementation guides.
- **D10 DEFAULT profile — Mark non-normative docs.** Any architecture-like document outside the normative owner registry must identify itself as non-normative instead of becoming an unregistered shadow owner. Default marker: `> **NON-NORMATIVE.**`
- **D11 DEFAULT profile — Explain problem, responsibility boundary, and forbidden outcome before jargon.**
- **D12 MUST when document/contract dependencies are machine-readable — Dependencies are semantic, not lexical.** A name mention is not an edge; record an edge only when the other owner's canonical type/derivation/lifecycle/result is required to implement this rule.
- **D13 MUST — No unmodeled anthropomorphism or semantic metaphor.** Do not give software artifacts intent, desire, knowledge, memory, judgment, or responsibility that the model does not define, and do not let decorative metaphor carry contract meaning. Name the actual state, policy, authority, observation, transition, or stored fact. Defined operations may use ordinary active voice.
- **D14 SHOULD — Use natural prose in the document's language.** Avoid unnecessary mixed-language noun chains and literal translations of foreign idioms. Keep standardized technical terms and code identifiers when exact spelling matters; prefer sentences that expose actor, action, condition, and consequence.
- **D15 MUST when translating, summarizing, splitting, or rewriting normative material — Preserve semantic force.** A transformation must not add or remove modality, scope, causality, fallback behavior, rationale, guarantees, or implementation assumptions. If semantics change, treat that as an explicit owner change with evidence, not as editorial cleanup.
- **D16 MUST — Make terminology and set semantics falsifiable.** Words such as robust, safe, fast, compatible, supported, and default need an operational contract when they affect behavior. Distinguish closed sets, extensible registries, currently supported subsets, and examples instead of letting prose blur them.
- **D17 MUST when a change specification is accepted — Integrate current semantics into canonical owners.** Change intent/specification remains provenance and rationale; it must not persist as a competing current semantic authority after the owning contracts are updated.
- **D18 MUST when implementation status is tracked — Separate status lifetimes.** Positive implementation facts, open gaps, and validation observations are different record classes. Resolved gaps leave the current gap registry; history belongs in version control/completion records, and Probe/readiness registries remain their own authorities while status derives summaries.
- **D19 SHOULD when status/TODO data can be derived from machine-readable registries — Prefer generated projections and structural growth control.** Root status/TODO views should derive from current facts, open gaps, missing gates, and readiness blockers instead of becoming independent truth. Shard detailed registries when needed; do not impose arbitrary line-count limits as a substitute for lifecycle design.

### D13 examples

Avoid:
- "The cache knows the value is stale."
- "The runtime wants to recover the session."
- "The document decides which backend to use."

Prefer:
- "The entry is stale when its revision is older than the current revision."
- "Recovery policy reconstructs the session after restart."
- "Backend selection follows `BackendSelectionPolicy`."

"The parser rejects invalid input" is fine if rejection is a defined operation.

## Comments and conventions

- **C1 DEFAULT profile — Comments are not architecture/history storage.** Architecture belongs in owning specs, tool usage in README, rationale in ADR/decision records, status in status/report, history in VCS.
- **C2 DEFAULT profile — Comment only to prevent local misreading.** Use comments for non-obvious constraints, externally forced shapes, safety reasoning, or intentional omissions; prefer clearer names/types/structure when possible.
- **C3 DEFAULT profile — No unstable references, change history, or code restatement in comments.**
- **C4 DEFAULT profile — One comment language.** Default: English.
- **C5 DEFAULT profile — Long-form Markdown in code comments is disabled by default.**
- **V1 DEFAULT profile — Formatter policy is a repository convention, not an architecture invariant.** Default: tool defaults, no repository-local override.
- **V2 DEFAULT profile — Canonical document-ID grammar is a repository convention.** Default: lowercase ASCII kebab case.
