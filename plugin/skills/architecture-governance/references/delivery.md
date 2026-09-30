# Delivery Rules

Load this file for change workflow, completion claims, or pre-release greenfield compatibility decisions.

## Change workflow

- **W1 MUST — Owner-first reconnaissance.** Before non-trivial implementation, inspect the owner, dependencies, canonical model, producers/consumers, lifecycle, failure path, and extension points relevant to the change.
- **W2 MUST — Semantic changes update every affected representation.** When a public semantic field/contract changes, inspect every representation that serializes, digests, compiles, reads, validates, or tests that meaning; use the project's dependency graph to determine the exact surface.

## Completion

- **G1 SHOULD — "It works" is not the whole definition of done.** Evaluate all applicable project quality requirements such as correctness, determinism, security, durability, accessibility, performance, and extensibility.
- **G2 MUST — Known in-scope architecture/spec violations cannot be closed as temporary debt.** If deliberately out of scope, leave them explicitly owned and tracked.

## Greenfield

- **F1 MUST when the product is pre-release and has no external compatibility/data obligations — Do not preserve speculative legacy.** Do not keep legacy/migration/compatibility layers solely to preserve a known-bad internal API. This rule does not apply once external users, public APIs, stored data, or deployed schemas create real compatibility obligations.
