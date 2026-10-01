# Architecture Governance

**English** · [한국어](README.ko.md)

Architecture Governance is a Claude Code skill for changes that are bigger than a local code edit.

Use it when a refactor, new subsystem, persistence layer, concurrency model, plugin boundary, or API change can affect who owns state, how operations are ordered, what survives a restart, or where failures are handled.

The skill makes Claude inspect those questions before proposing another manager, registry, cache, dispatcher, adapter, or workaround.

## Install

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

Start a new Claude Code session after installation.

## When it helps

Typical cases include:

- designing or reviewing a subsystem
- planning a large refactor
- cleaning up an architecture or protocol specification
- introducing persistence, retries, cancellation, or concurrency
- defining plugin, process, trust, or capability boundaries
- deciding whether a problem is local implementation debt or a flaw in the design

## What it looks for

The rules are built around practical failure modes:

- two places both acting as the source of truth
- a new abstraction duplicating an existing owner
- behavior that depends on registration order, callback timing, container iteration, or thread scheduling
- identity, equality, authority, lifecycle, retry, or failure semantics left implicit
- caches or projections quietly becoming authoritative state
- cancellation being mistaken for completion of an external operation
- fallbacks, limits, and timeouts appearing without a clear owner
- tests that prove the happy path but never try to break the contract

It does not prescribe a framework or architecture style. It works from the project's existing model and asks whether that model is explicit, internally consistent, and testable.

## Files

The detailed rules are split into five groups so Claude only needs to read the parts relevant to the current task:

- `system.md` — ownership, abstractions, runtime behavior, state, persistence, security
- `decisions.md` — ambiguous requirements and engineering vs. product decisions
- `writing.md` — specifications, terminology, comments, and normative language
- `evidence.md` — tests, probes, readiness, concurrency, security, and performance evidence
- `delivery.md` — change workflow, completion criteria, and greenfield compatibility

`SKILL.md` contains the short working procedure and the defaults that apply across those areas.

## Validation

```bash
python plugin/skills/architecture-governance/scripts/validate.py
python tests/validate_repository.py
```

These checks catch repository-structure and rule-set mistakes. They are not a substitute for reviewing the actual design.

## Rule index

[Engineering Constitution](doctrine/ENGINEERING_CONSTITUTION.md)

## License

[Apache-2.0](LICENSE)
