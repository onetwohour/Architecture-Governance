#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys

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
    SKILL / "SKILL.md",
    SKILL / "references" / "index.md",
    SKILL / "references" / "system.md",
    SKILL / "references" / "decisions.md",
    SKILL / "references" / "writing.md",
    SKILL / "references" / "evidence.md",
    SKILL / "references" / "delivery.md",
    SKILL / "references" / "aliases.json",
    SKILL / "references" / "source-traceability.json",
    SKILL / "archive" / "v1.1" / "rule-registry-v1.1.ko.json",
]
for p in required:
    req(p.exists(), f"missing {p.relative_to(ROOT)}")

manifest_path = ROOT / "plugin" / ".claude-plugin" / "plugin.json"
if manifest_path.exists():
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    req(m.get("name") == "architecture-governance", "manifest name mismatch")
    req(m.get("version") == "1.3.0", "manifest version mismatch")

validator_path = SKILL / "scripts" / "validate.py"
if validator_path.exists():
    proc = subprocess.run([sys.executable, str(validator_path)], cwd=SKILL, text=True, capture_output=True)
    if proc.returncode != 0:
        errors.append("skill validator failed:\n" + proc.stdout + proc.stderr)

if errors:
    print("FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("PASS")
print("repository=Architecture-Governance")
print("version=1.3.0")
