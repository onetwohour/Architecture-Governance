#!/usr/bin/env python3
"""Validate plugin structure and active policy inventory; not target semantics."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT.parents[1]
errors = []


def req(cond, msg):
    if not cond:
        errors.append(msg)


skill = ROOT / "SKILL.md"
skill_text = skill.read_text(encoding="utf-8") if skill.exists() else ""
req(skill.exists(), "SKILL.md missing")
req(skill_text.startswith("---\n"), "SKILL.md must start with frontmatter")
req(bool(re.search(r"^name:\s*architecture-governance\s*$", skill_text, re.M)), "skill name mismatch")
req(bool(re.search(r"^argument-hint:\s*.+$", skill_text, re.M)), "argument hint missing")
req(len(skill_text.encode("utf-8")) <= 5200,
    f"SKILL.md too large: {len(skill_text.encode('utf-8'))} bytes")
req(not re.search(r"[가-힣]", skill_text), "SKILL.md must be English")

manifest_path = PLUGIN / ".claude-plugin" / "plugin.json"
req(manifest_path.exists(), "plugin manifest missing")
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    req(manifest.get("name") == "architecture-governance", "plugin name mismatch")

refs = {name: ROOT / "references" / f"{name}.md"
        for name in ("system", "decisions", "writing", "evidence", "delivery")}
workflows = ("plan", "implement", "audit", "verify", "project-governance", "adopt")
for name in workflows:
    path = ROOT / "workflows" / f"{name}.md"
    req(path.exists(), f"missing workflows/{name}.md")
    req(f"workflows/{name}.md" in skill_text, f"unrouted workflow {name}")
for name in ("change_scope.py", "run_validation.py", "project_state.py", "impact.py"):
    req((ROOT / "scripts" / name).exists(), f"missing scripts/{name}")
req((ROOT / "references" / "project-state-format.md").exists(), "missing project-state-format reference")
for name in ("architecture-review.md", "contract.md", "decision-record.md",
             "probe.md", "change-scope.json"):
    req((ROOT / "templates" / name).exists(), f"missing template {name}")

active_strength = {}
for name, path in refs.items():
    req(path.exists(), f"missing references/{name}.md")
    if not path.exists():
        continue
    content = path.read_text(encoding="utf-8")
    req(not re.search(r"[가-힣]", content), f"{name}.md must be English")
    for rid, strength in re.findall(
        r"\*\*([WOASTXJDCEGVF]\d+)\s+(MUST|SHOULD|DEFAULT)\b", content
    ):
        req(rid not in active_strength, f"duplicate compact rule ID {rid}")
        active_strength[rid] = strength

expected = (
    {f"W{i}" for i in range(1, 3)}
    | {f"O{i}" for i in range(1, 13)}
    | {"A1"}
    | {f"S{i}" for i in range(1, 28)}
    | {f"T{i}" for i in range(1, 3)}
    | {f"X{i}" for i in range(1, 3)}
    | {f"J{i}" for i in range(1, 12)}
    | {f"D{i}" for i in range(1, 20)}
    | {f"C{i}" for i in range(1, 6)}
    | {f"V{i}" for i in range(1, 3)}
    | {f"E{i}" for i in range(1, 16)}
    | {f"G{i}" for i in range(1, 3)}
    | {"F1"}
)
req(set(active_strength) == expected,
    f"active rule set mismatch: missing={sorted(expected-set(active_strength))}, "
    f"extra={sorted(set(active_strength)-expected)}")
req(len(active_strength) == 101, f"expected 101 active rules, found {len(active_strength)}")
req(active_strength.get("O12") == "SHOULD", "O12 strength must be SHOULD")

if errors:
    print("FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("PASS")
print(f"active_rules={len(active_strength)}")
print(f"skill_bytes={len(skill_text.encode('utf-8'))}")
print("workflows=5")
print("policy_surface=5 reference files")
print("proof_scope=current repository structure and active rule-set integrity")
print("does_not_prove=target-project design or runtime correctness")
