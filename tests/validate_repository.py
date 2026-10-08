#!/usr/bin/env python3
"""Repository shape validation; substantive checks live in separate tests."""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugin" / "skills" / "architecture-governance"
errors = []


def req(cond, msg):
    if not cond:
        errors.append(msg)


required = [
    ROOT / "README.md",
    ROOT / "README.ko.md",
    ROOT / "doctrine" / "ENGINEERING_CONSTITUTION.md",
    ROOT / "plugin" / ".claude-plugin" / "plugin.json",
    ROOT / "tests" / "test_governance_runtime.py",
    ROOT / "tests" / "test_project_state.py",
    ROOT / "tests" / "test_impact.py",
    ROOT / "doctrine" / "POLICY_REVIEW.md",
    SKILL / "SKILL.md",
    *[SKILL / "references" / f"{name}.md" for name in
      ("index", "system", "decisions", "writing", "evidence", "delivery", "project-state-format")],
    *[SKILL / "workflows" / f"{name}.md" for name in
      ("plan", "implement", "audit", "verify", "project-governance", "adopt")],
    *[SKILL / "scripts" / name for name in
      ("validate.py", "change_scope.py", "run_validation.py", "project_state.py", "impact.py")],
    SKILL / "templates" / "change-scope.json",
]
for path in required:
    req(path.exists(), f"missing {path.relative_to(ROOT)}")

manifest_path = ROOT / "plugin" / ".claude-plugin" / "plugin.json"
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    req(manifest.get("name") == "architecture-governance", "manifest name mismatch")

validator = SKILL / "scripts" / "validate.py"
if validator.exists():
    proc = subprocess.run([sys.executable, str(validator)], cwd=SKILL,
                          text=True, capture_output=True)
    if proc.returncode != 0:
        errors.append("skill validator failed:\n" + proc.stdout + proc.stderr)

if errors:
    print("FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("PASS")
print("repository=Architecture-Governance")
print("proof_scope=repository shape and skill rule-set checks")
