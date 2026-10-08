# Adopt this skill in a target repository

This plugin is **not** the project's architecture registry, CI, test framework or issue tracker.

1. Inspect the project's existing normative architecture, contribution policy, test commands, CI, language tooling and generated files. Adopt the existing names rather than imposing The Note's folders on unrelated projects.
2. Point engineers/agents from their existing project instructions to `architecture-governance`. Keep those instructions short; do not copy the 101 rules or reproduce normative contract definitions.
3. Use `plan` for cross-boundary changes, `implement` for delivery, `audit`/`review` for independent challenge and `verify` for real checks. Scale depth to risk.
4. **Enforcement is separate from guidance.** Integrate repository-native dependency/architecture checks and adversarial tests into its own CI. Keep required branch protection in that repository. An LLM skill and a local scope plan cannot prevent all unwanted writes or certify semantics.
5. Optionally create an ephemeral plan for `change_scope.py`. List generated files under `protected_paths` *only where they are actually generated*. Never globally assume STATUS.md or TODO.md must be generated.
6. Run the validation helper only when a portable evidence record helps. Avoid committing logs or JSON artifacts unless the project's evidence retention policy explicitly calls for it.

## The Note example (not a universal dependency)

A The Note integration should resolve its existing normative owners, `architecture.toml`, `probes.toml`, `readiness.toml`, Rust workspace tests and architecture lint. It must not create parallel definitions of those facts inside this skill.

**Acceptance:** an unplanned path is flagged for review, a failing check records FAIL, and semantic compliance is never inferred solely from paths, test markers or green scripts.
