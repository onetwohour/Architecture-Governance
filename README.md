# Architecture Governance

**English** · [한국어](README.ko.md)

A Claude Code skill for architecture and specification work. It emphasizes semantic ownership, explicit contracts, deterministic ordering, evidence-backed probes, and disciplined completion.

## Install

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

Start a new Claude Code session after installation.

## Token-efficient layout

The model-facing entry point is intentionally small. `SKILL.md` contains only the default workflow and hard invariants. Detailed rules are loaded on demand:

- `system.md` — ownership, abstraction, runtime semantics, state, persistence, security
- `decisions.md` — ambiguity and product-vs-engineering decisions
- `writing.md` — specs, comments, terminology, anti-anthropomorphism
- `evidence.md` — probes, readiness, security/performance evidence
- `delivery.md` — change workflow, completion, greenfield compatibility

Rules use compact IDs such as `O3` instead of `R-OWN-003`. All previous IDs, source citations, and the complete v1.1 wording are preserved under `aliases.json` and `archive/v1.1/`; normal runs do not load them.

## Core behavior

- Find the existing semantic owner before creating a new manager/store/registry/dispatcher.
- Keep one normative authority per semantic responsibility.
- Make correctness-relevant dependency and ordering explicit.
- Close identity, ownership, state, transition, authority, failure/retry, persistence, concurrency, and other applicable contract dimensions.
- Treat current code as implementation evidence, not automatic architecture authority.
- Validate important invariants with negative cases and forbidden observable states.
- Do not anthropomorphize software with unmodeled intent, knowledge, memory, or judgment.
- Use stable semantic references, not positional section numbers.
- Do not claim readiness or completion without evidence.

## Local validation

```bash
python plugin/skills/architecture-governance/scripts/validate.py
python tests/validate_repository.py
```

## Full policy

[Engineering Constitution](doctrine/ENGINEERING_CONSTITUTION.md)

## License

[Apache-2.0](LICENSE)
