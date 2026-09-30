# Architecture Governance

**English** · [한국어](README.ko.md)

**Architecture Governance** is a Claude Code plugin for designing, reviewing, and changing non-trivial software architecture without losing semantic ownership, contract boundaries, documentation authority, or verification evidence.

It turns architecture work into a traceable discipline: find the semantic owner, distinguish design truth from implementation truth, reuse before creating parallel systems, close the contract, make hidden ordering explicit, validate negative paths, and require evidence before declaring readiness or completion.

## Installation

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

Start a new Claude Code session after installation.

## Usage

No separate command is required. Ask for architecture or implementation work normally.

```text
Review this subsystem and find ownership, lifecycle, and contract defects before changing it.
```

```text
Turn these design notes into an authoritative specification and define probes for the important invariants.
```

```text
Refactor this feature without creating a second manager, store, dispatcher, or source of truth.
```

The skill stays lightweight for ordinary work and becomes stricter when a task touches semantic ownership, persistence, concurrency, failure/retry, external effects, architecture changes, specification authority, or shared abstractions.

## Core ideas

- One semantic responsibility has one normative authority.
- Reuse before create; a new indirection carries the burden of proof.
- Current code is implementation evidence, not automatic architecture authority.
- Normative architecture, implementation status, roadmap, and research remain distinct.
- Stable semantic references use a path plus a concept/rule identity, not positional section references such as `§12`.
- Correctness-relevant dependency and ordering must be explicit rather than hidden in registration order, container iteration, thread timing, or callback order.
- Important contracts close identity, ownership, state, lifecycle, authority, failure, retry, persistence, concurrency, and observability where applicable.
- Serious validation includes negative paths and forbidden observable states.
- Readiness and completion are evidence-backed claims.

## Full constitution

The complete readable constitution is available at [doctrine/ENGINEERING_CONSTITUTION.md](doctrine/ENGINEERING_CONSTITUTION.md). The canonical machine-readable rule registry used by the skill is at [`plugin/skills/architecture-governance/references/rule-registry.json`](plugin/skills/architecture-governance/references/rule-registry.json).

## Local usage

To run the plugin from a clone without installing it:

```bash
git clone https://github.com/onetwohour/Architecture-Governance.git
claude --plugin-dir ./Architecture-Governance/plugin
```

`--plugin-dir` applies to that session only.

## Validation

```bash
python plugin/skills/architecture-governance/scripts/validate.py
python tests/validate_repository.py
```

## License

[Apache-2.0](LICENSE)
