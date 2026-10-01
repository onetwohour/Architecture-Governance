#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

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
req(re.search(r"^name:\s*architecture-governance\s*$", skill_text, re.M), "skill name mismatch")
req(len(skill_text.encode("utf-8")) <= 5200, f"SKILL.md too large: {len(skill_text.encode('utf-8'))} bytes")
req(not re.search(r"[가-힣]", skill_text), "SKILL.md must be English")

manifest_path = PLUGIN / ".claude-plugin" / "plugin.json"
req(manifest_path.exists(), "plugin manifest missing")
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    req(manifest.get("name") == "architecture-governance", "plugin name mismatch")

refs = {
    "system": ROOT / "references" / "system.md",
    "decisions": ROOT / "references" / "decisions.md",
    "writing": ROOT / "references" / "writing.md",
    "evidence": ROOT / "references" / "evidence.md",
    "delivery": ROOT / "references" / "delivery.md",
}

active_strength = {}
for name, path in refs.items():
    req(path.exists(), f"missing references/{name}.md")
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    req(not re.search(r"[가-힣]", text), f"{name}.md must be English")
    for rid, strength in re.findall(r"\*\*([WOASTXJDCEGVF]\d+)\s+(MUST|SHOULD|DEFAULT)\b", text):
        req(rid not in active_strength, f"duplicate compact rule ID {rid}")
        active_strength[rid] = strength

expected = (
    {f"W{i}" for i in range(1,3)}
    | {f"O{i}" for i in range(1,13)}
    | {"A1"}
    | {f"S{i}" for i in range(1,28)}
    | {f"T{i}" for i in range(1,3)}
    | {f"X{i}" for i in range(1,3)}
    | {f"J{i}" for i in range(1,12)}
    | {f"D{i}" for i in range(1,20)}
    | {f"C{i}" for i in range(1,6)}
    | {f"V{i}" for i in range(1,3)}
    | {f"E{i}" for i in range(1,16)}
    | {f"G{i}" for i in range(1,3)}
    | {"F1"}
)
req(set(active_strength) == expected,
    f"active rule set mismatch: missing={sorted(expected-set(active_strength))}, extra={sorted(set(active_strength)-expected)}")
req(len(active_strength) == 101, f"expected 101 active rules, found {len(active_strength)}")
req(active_strength.get("O12") == "SHOULD", "O12 strength must be SHOULD")

if errors:
    print("FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("PASS")
print(f"active_rules={len(active_strength)}")
print(f"skill_bytes={len(skill_text.encode('utf-8'))}")
print("policy_surface=5 reference files")
print("proof_scope=current repository structure and active rule-set integrity")
print("does_not_prove=semantic correctness beyond the checks above")
