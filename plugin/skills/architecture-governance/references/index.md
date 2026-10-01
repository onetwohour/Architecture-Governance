# Reference Index

Model-facing policy is split so normal runs load only what they need.

| File | Load for |
| --- | --- |
| `system.md` | ownership, abstraction, runtime semantics, state, persistence, security |
| `decisions.md` | ambiguity, design choices, escalation to product decisions |
| `writing.md` | specs, docs, comments, wording, references |
| `evidence.md` | probes, tests, readiness, security/performance evidence |
| `delivery.md` | change workflow, completion, greenfield compatibility |

Compact ID prefixes: W work, O ownership, A abstraction, S runtime semantics, T data, X security, J decisions, D documentation, C comments, V conventions, E evidence, G completion, F greenfield.

Do not load `../archive/*`, `aliases.json`, or `source-traceability.json` during normal work. `aliases.json` preserves the legacy 83-rule mapping; `source-traceability.json` records the 94-rule source-methodology disposition used for fidelity audits.
