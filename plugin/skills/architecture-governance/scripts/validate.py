#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT.parents[1]
ARCHIVE = ROOT / "archive" / "v1.1"
errors = []

def req(cond, msg):
    if not cond:
        errors.append(msg)

skill = ROOT / "SKILL.md"
req(skill.exists(), "SKILL.md missing")
skill_text = skill.read_text(encoding="utf-8") if skill.exists() else ""
req(skill_text.startswith("---\n"), "SKILL.md must start with frontmatter")
req(re.search(r"^name:\s*architecture-governance\s*$", skill_text, re.M), "skill name mismatch")
req(len(skill_text.encode("utf-8")) <= 4500, f"SKILL.md too large: {len(skill_text.encode('utf-8'))} bytes")
req(not re.search(r"[가-힣]", skill_text), "SKILL.md must be English")
req(not re.search(r"R-[A-Z]+-\d{3}", skill_text), "SKILL.md must not use legacy long rule IDs")

manifest_path = PLUGIN / ".claude-plugin" / "plugin.json"
req(manifest_path.exists(), "plugin manifest missing")
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    req(manifest.get("version") == "1.2.0", "plugin version must be 1.2.0")

refs = {
    "system": ROOT / "references" / "system.md",
    "decisions": ROOT / "references" / "decisions.md",
    "writing": ROOT / "references" / "writing.md",
    "evidence": ROOT / "references" / "evidence.md",
    "delivery": ROOT / "references" / "delivery.md",
}
for name, path in refs.items():
    req(path.exists(), f"missing references/{name}.md")
    if path.exists():
        text = path.read_text(encoding="utf-8")
        req(not re.search(r"[가-힣]", text), f"{name}.md must be English")
        req(not re.search(r"R-[A-Z]+-\d{3}", text), f"{name}.md uses legacy long rule IDs")

active = []
for path in refs.values():
    if path.exists():
        active += re.findall(r"\*\*([WOASTXJDCEGVF]\d+)\s+(?:MUST|SHOULD|DEFAULT)\b", path.read_text(encoding="utf-8"))
req(len(active) == 83, f"expected 83 active rules, found {len(active)}")
req(len(active) == len(set(active)), "duplicate compact rule IDs")

aliases_path = ROOT / "references" / "aliases.json"
req(aliases_path.exists(), "aliases.json missing")
if aliases_path.exists():
    aliases = json.loads(aliases_path.read_text(encoding="utf-8")).get("rules", [])
    alias_ids = [r.get("id") for r in aliases]
    req(len(aliases) == 83, f"expected 83 alias entries, found {len(aliases)}")
    req(set(alias_ids) == set(active), "active rule IDs and alias IDs differ")
    current_ids = [r.get("current_id") for r in aliases]
    req(len(current_ids) == len(set(current_ids)), "duplicate current IDs in aliases")
    for r in aliases:
        req(r.get("current_id") in r.get("aliases", []), f"{r.get('id')}: current_id missing from aliases")
        req(bool(r.get("sources")), f"{r.get('id')}: source provenance missing")

legacy_registry = ARCHIVE / "rule-registry-v1.1.ko.json"
req(legacy_registry.exists(), "archived v1.1 registry missing")
if legacy_registry.exists() and aliases_path.exists():
    old_rules = json.loads(legacy_registry.read_text(encoding="utf-8")).get("rules", [])
    req(len(old_rules) == 83, f"archived registry must contain 83 rules, found {len(old_rules)}")
    old_ids = {r.get("id") for r in old_rules}
    mapped_ids = {r.get("current_id") for r in json.loads(aliases_path.read_text(encoding="utf-8")).get("rules", [])}
    req(old_ids == mapped_ids, "archived registry IDs are not fully mapped")

writing = refs["writing"].read_text(encoding="utf-8") if refs["writing"].exists() else ""
req("D13 MUST" in writing and "anthropomorphism" in writing.lower(), "D13 anthropomorphism rule missing")
req("D14 SHOULD" in writing and "natural prose" in writing.lower(), "D14 natural prose rule missing")

for rel in ["archive/rule-registry-v1.1.ko.json", "references/aliases.json"]:
    req((ROOT / rel).exists(), f"missing {rel}")

if errors:
    print("FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("PASS")
print(f"active_rules={len(active)}")
print(f"skill_bytes={len(skill_text.encode('utf-8'))}")
print("legacy_rules=83 preserved")
