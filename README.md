# Architecture Governance

**English** · [한국어](README.ko.md)

**Make changes to a codebase without losing track of its architecture.**

Architecture Governance is a Claude Code plugin for planning, implementing, reviewing, and verifying software changes against a project's existing design. It helps an agent understand who owns a behavior, where a change belongs, and what evidence is needed before calling the work complete.

It does not impose a new architecture. The project's own specifications, contracts, and tests remain authoritative.

## Why use it?

A change can compile, pass a few tests, and still violate a system's design: introduce a second source of truth, bypass a public contract, invent an error-handling policy, or mistake a successful command for proof of correctness.

Architecture Governance brings those questions into the development workflow:

- **Find the owner.** Identify the existing responsibility and its contract before adding another abstraction.
- **Understand the behavior.** Examine state, identity, ordering, failures, recovery, and dependency boundaries where relevant.
- **Plan proportionately.** Keep small edits small; scrutinize changes to public contracts and system-wide rules.
- **Challenge the change.** Review the actual diff and test failure paths, not just the happy path.
- **Report evidence.** Distinguish what was specified, implemented, executed, and actually demonstrated.

## Install

In Claude Code:

```bash
claude plugin marketplace add onetwohour/claude-plugins
claude plugin install architecture-governance@onetwohour
```

Start a new Claude Code session after installing.

## Get started

Use the skill with a task:

```text
/architecture-governance:architecture-governance plan Design a safe recovery path after a failed save
```

To implement a change:

```text
/architecture-governance:architecture-governance implement Fix stale responses after editor reconfiguration
```

To examine an existing system or change:

```text
/architecture-governance:architecture-governance audit Review architecture documents and their implementation
/architecture-governance:architecture-governance review Review my current Git diff
```

The skill can also be selected automatically for relevant work. Explicit invocation is useful when you want a particular workflow.

## Workflows

| Mode | What it does |
| --- | --- |
| `plan` | Identifies owners, contracts, alternatives, impact, and a verification plan. |
| `implement` | Makes the change with owner-first analysis, diff review, and relevant checks. |
| `audit` | Looks for architecture violations, including contradictions in the design documents themselves. |
| `review` | Compares proposed or actual changes with architectural obligations. |
| `verify` | Runs applicable checks and explains the evidence and remaining gaps. |
| `project` | Helps derive project-status and outstanding-work views from existing sources. |
| `adopt` | Helps integrate the workflow into an existing repository and its checks. |

All modes belong to **one skill**. Without an explicit mode, the default is `plan` unless the task clearly calls for something else.

## What it does not promise

Architecture Governance guides an agent's engineering process; it is not a substitute for your project's architecture linter, test suite, security enforcement, or CI. A skill may not be invoked on every change, and no text-based review can establish every semantic invariant.

Likewise, finding a test or recording a successful command is not the same as proving its full contract. Unchecked or inconclusive results should remain visible rather than being reported as complete.

For enforceable guarantees, keep architecture checks and tests in your **project's own CI**.

## Documentation

- [Optional tools and advanced usage](docs/TOOLS.md)
- [Engineering principles](doctrine/ENGINEERING_CONSTITUTION.md)
- [Contributing and development](CONTRIBUTING.md)

## License

[Apache-2.0](LICENSE)
