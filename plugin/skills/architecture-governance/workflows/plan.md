# Plan: understand the owner before touching code

**Purpose.** Prevent an implementation shortcut from silently changing the project's model. Do not mistake planning for an authorization to invent normative requirements.

1. **Map the real authority.** Locate the target project's instructions and normative owner registry, if any. Read the owning specification and direct normative dependencies. If no formal registry exists, infer the current authority carefully from documented public contracts and code; mark ambiguities rather than inventing one.
2. **Map the mechanism.** Trace entry points, producers, consumers, state authority, persistence/IO, lifecycle, concurrency boundaries, failure and cancellation paths, dependency directions and extension points *as relevant*. Distinguish durable truth from projections and caches.
3. **Classify the decision.** Is the requested behavior already specified? Is it implementation freedom? Is an owner incomplete or wrong? Would fixing it alter a system-wide law? Is it truly a product-policy tradeoff? Consult `references/decisions.md`; escalate only a genuine unresolved policy choice.
4. **Test alternatives.** Compare reuse/owner repair, contract extension and new abstraction against authority duplication, additional truth, ordering assumptions and failure semantics. Do not select by convenience or smallest diff alone.
5. **Choose change tier.** LOCAL = contained change with no observable contract change. CONTRACT = public owner-local semantics or multiple dependent consumers. ARCHITECTURE = closed law, trust/authority boundary, persistent truth or system-wide ordering. Tier is determined by semantic effect, not line count.
6. **Describe the plan.** State expected paths and reason for each; normative owners affected; invariants/forbidden states; evidence to run; compatibility/data obligations; unclear items; rollback or recovery concerns where pertinent.
7. **Record the review checkpoint.** An unexpected new owner, changed dependency direction, new fallback/timeout, altered public contract or additional protected path means re-evaluate this plan before proceeding.

The path plan can be recorded as short-lived JSON for `change_scope.py`:

```json
{
  "allowed_paths": ["src/**", "tests/**", "Cargo.toml"],
  "protected_paths": ["STATUS.md", "TODO.md"],
  "reason": "Example scope only; adapt to the target project"
}
```

The tool does not determine whether a design is correct. Glob patterns are matched against repository-relative POSIX paths; Python `fnmatch` wildcards may also span directory separators. Review broad patterns carefully. Do not copy this example into the target repository as an architecture authority.

**Output:** a short rationale-led plan; for local edits use a few lines, for system-wide law changes use a full contract and counterexample.
