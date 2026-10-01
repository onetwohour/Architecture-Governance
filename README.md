# Architecture Governance

**English** · [한국어](README.ko.md)

Architecture problems are rarely caused by a missing class or function. They usually come from unclear ownership, duplicated sources of truth, hidden ordering, underspecified failure behavior, or abstractions that were introduced before the system actually needed them.

Architecture Governance is a Claude Code skill for reviewing and changing software architecture without papering over those problems.

It is useful when you are designing a subsystem, cleaning up a specification, planning a large refactor, introducing persistence or concurrency, defining plugin boundaries, or trying to decide whether a problem belongs in the implementation or in the architecture itself.

## Install

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

Start a new Claude Code session after installation.

## What it checks

The skill pushes architecture work toward a few concrete questions:

- Who owns this semantic decision?
- Is the same fact stored or decided in more than one place?
- Are dependencies and ordering explicit, or are they leaking through registration order, container order, callbacks, or thread timing?
- Are identity, equality, authority, state transitions, failure, retry, persistence, and reconfiguration actually defined?
- Does an abstraction have enough evidence to exist, or is it just another layer?
- Can important guarantees be falsified with a negative test or probe?
- Is the implementation working around a broken owner instead of fixing it?

The goal is not to impose a particular architecture. The skill uses the project's own domain model and tries to make its rules explicit, minimal, and testable.

## How it is organized

`SKILL.md` contains the working loop and the strongest defaults. More detailed rules are split by concern and loaded only when relevant:

- `system.md` — ownership, abstraction, runtime semantics, state, persistence, security
- `decisions.md` — ambiguous requirements and engineering-vs-product decisions
- `writing.md` — specifications, terminology, comments, and normative language
- `evidence.md` — probes, readiness, concurrency, security, and performance evidence
- `delivery.md` — change workflow, completion criteria, and greenfield compatibility

The five reference files are the active policy.

## Validation

```bash
python plugin/skills/architecture-governance/scripts/validate.py
python tests/validate_repository.py
```

The validator checks the repository structure and active rule set. Passing it does not by itself prove that a design is semantically correct.

## Policy index

[Engineering Constitution](doctrine/ENGINEERING_CONSTITUTION.md)

## License

[Apache-2.0](LICENSE)
