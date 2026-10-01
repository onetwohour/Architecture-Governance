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
skill_text = skill.read_text(encoding="utf-8") if skill.exists() else ""
req(skill.exists(), "SKILL.md missing")
req(skill_text.startswith("---\n"), "SKILL.md must start with frontmatter")
req(re.search(r"^name:\s*architecture-governance\s*$", skill_text, re.M), "skill name mismatch")
req(len(skill_text.encode("utf-8")) <= 5200, f"SKILL.md too large: {len(skill_text.encode('utf-8'))} bytes")
req(not re.search(r"[가-힣]", skill_text), "SKILL.md must be English")
req(not re.search(r"R-[A-Z]+-\d{3}", skill_text), "SKILL.md must not use legacy long rule IDs")

manifest_path = PLUGIN / ".claude-plugin" / "plugin.json"
req(manifest_path.exists(), "plugin manifest missing")
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    req(manifest.get("version") == "1.3.0", "plugin version must be 1.3.0")

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
    req(not re.search(r"R-[A-Z]+-\d{3}", text), f"{name}.md uses legacy long rule IDs")
    for rid, strength in re.findall(r"\*\*([WOASTXJDCEGVF]\d+)\s+(MUST|SHOULD|DEFAULT)\b", text):
        req(rid not in active_strength, f"duplicate compact rule ID {rid}")
        active_strength[rid] = strength

req(len(active_strength) == 101, f"expected 101 active rules, found {len(active_strength)}")

aliases_path = ROOT / "references" / "aliases.json"
req(aliases_path.exists(), "aliases.json missing")
alias_rules = json.loads(aliases_path.read_text(encoding="utf-8")).get("rules", []) if aliases_path.exists() else []
req(len(alias_rules) == 83, f"expected 83 legacy alias entries, found {len(alias_rules)}")
req({r.get("id") for r in alias_rules}.issubset(active_strength), "legacy alias IDs must remain active")

legacy_registry = ARCHIVE / "rule-registry-v1.1.ko.json"
req(legacy_registry.exists(), "archived v1.1 registry missing")
if legacy_registry.exists() and alias_rules:
    old_rules = json.loads(legacy_registry.read_text(encoding="utf-8")).get("rules", [])
    req(len(old_rules) == 83, f"archived registry must contain 83 rules, found {len(old_rules)}")
    old_by_id = {r.get("id"): r for r in old_rules}
    req(set(old_by_id) == {r.get("current_id") for r in alias_rules}, "archived registry IDs are not fully mapped")
    for a in alias_rules:
        old = old_by_id.get(a.get("current_id"))
        if old:
            req(active_strength.get(a.get("id")) == old.get("strength"),
                f"{a.get('id')}: compact rewrite changed strength {old.get('strength')} -> {active_strength.get(a.get('id'))}")

trace_path = ROOT / "references" / "source-traceability.json"
req(trace_path.exists(), "source-traceability.json missing")
if trace_path.exists():
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    rules = trace.get("rules", [])
    req([r.get("id") for r in rules] == [f"G-{i:03d}" for i in range(1,95)],
        "traceability must contain G-001..G-094 in order")
    meta = trace.get("reference_corpus", {})
    req(meta.get("files") == 50, "reference corpus file count must be 50")
    req(meta.get("lines") == 23294, "reference corpus line count mismatch")
    req(meta.get("generalized_rules") == 94, "generalized rule count mismatch")
    req(meta.get("active_policy_rules") == len(active_strength), "trace active rule count mismatch")
    audit_only, external = set(), set()
    for r in rules:
        d, refs_ = r.get("disposition"), r.get("active_rules", [])
        if d == "active":
            req(bool(refs_), f"{r.get('id')}: active mapping missing")
            for rid in refs_:
                req(rid in active_strength, f"{r.get('id')}: unknown active rule {rid}")
        elif d == "skill":
            req(refs_ == ["SKILL"], f"{r.get('id')}: skill mapping must be SKILL")
        elif d == "audit-only":
            audit_only.add(r.get("id"))
            req(not refs_, f"{r.get('id')}: audit-only rule must not claim active policy")
        elif d == "external-workflow":
            external.add(r.get("id"))
            req(not refs_, f"{r.get('id')}: external workflow rule must not claim source policy")
        else:
            req(False, f"{r.get('id')}: invalid disposition {d}")
    req(audit_only == {"G-090","G-091","G-094"}, f"unexpected audit-only set: {sorted(audit_only)}")
    req(external == {"G-009"}, f"unexpected external-workflow set: {sorted(external)}")

req(active_strength.get("O12") == "SHOULD", "O12 must preserve v1.1 SHOULD strength")
for rid in [f"S{i}" for i in range(17,28)] + ["X2"] + [f"D{i}" for i in range(15,20)] + ["E15"]:
    req(rid in active_strength, f"{rid}: restored rule missing")

if errors:
    print("FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)

print("PASS")
print(f"active_rules={len(active_strength)}")
print("legacy_rules=83 preserved")
print("generalized_rules=94 traced")
print(f"skill_bytes={len(skill_text.encode('utf-8'))}")
print("proof_scope=repository structure, legacy strength preservation, explicit 94-rule disposition")
print("does_not_prove=semantic equivalence beyond recorded mappings and source evidence")
