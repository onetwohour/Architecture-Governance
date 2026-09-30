#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT.parents[1]
errors = []

def req(cond, msg):
    if not cond:
        errors.append(msg)

skill = ROOT / 'SKILL.md'
req(skill.exists(), 'SKILL.md missing')
text = skill.read_text(encoding='utf-8') if skill.exists() else ''
req(text.startswith('---\n'), 'SKILL.md must start with YAML frontmatter')
req(re.search(r'^name:\s*architecture-governance\s*$', text, re.M), 'skill name mismatch')
req(re.search(r'^description:\s*.+$', text, re.M), 'skill description missing')

manifest_path = PLUGIN_ROOT / '.claude-plugin' / 'plugin.json'
req(manifest_path.exists(), '.claude-plugin/plugin.json missing')
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    req(manifest.get('$schema') == 'https://json.schemastore.org/claude-code-plugin-manifest.json', 'Claude plugin schema mismatch')
    req(manifest.get('name') == 'architecture-governance', 'plugin name mismatch')
    req(manifest.get('version') == '1.1.0', 'plugin version mismatch')
    req(manifest.get('repository') == 'https://github.com/onetwohour/Architecture-Governance', 'repository metadata mismatch')

registry_path = ROOT / 'references' / 'rule-registry.json'
req(registry_path.exists(), 'rule-registry.json missing')
rules = []
if registry_path.exists():
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    rules = registry.get('rules', [])
    ids = [r.get('id') for r in rules]
    req(len(rules) == 83, f'expected 83 canonical rules, found {len(rules)}')
    req(len(ids) == len(set(ids)), 'duplicate rule IDs')
    req('R-DOC-013' in ids, 'anthropomorphism rule missing')
    req('R-DOC-014' in ids, 'natural technical prose rule missing')
    for r in rules:
        for key in ['id','title','category','statement','rationale','portability','strength','enforcement']:
            req(bool(r.get(key)), f"{r.get('id','?')}: missing {key}")
        req(r.get('portability') in {'CORE','CONDITIONAL','PROFILE'}, f"{r.get('id')}: invalid portability")
        req(r.get('strength') in {'MUST','SHOULD','DEFAULT'}, f"{r.get('id')}: invalid strength")
        if r.get('portability') == 'CONDITIONAL':
            req(bool(r.get('applies_when')), f"{r.get('id')}: conditional rule missing applies_when")

known_ids = {r.get('id') for r in rules}
constitution = ROOT / 'references' / 'engineering-constitution.md'
req(constitution.exists(), 'engineering-constitution.md missing')
if constitution.exists():
    constitution_text = constitution.read_text(encoding='utf-8')
    projected_ids = set(re.findall(r'^## (R-[A-Z]+-\d{3})\b', constitution_text, re.M))
    req(projected_ids == known_ids, f'constitution/registry ID mismatch: missing={sorted(known_ids-projected_ids)} extra={sorted(projected_ids-known_ids)}')

for name in ['editorial-policy.md','decision-policy.md','completion-gates.md','anti-patterns.md','rule-model.md']:
    p = ROOT / 'references' / name
    req(p.exists(), f'missing references/{name}')
    if p.exists():
        for rid in re.findall(r'^## (R-[A-Z]+-\d{3})\b', p.read_text(encoding='utf-8'), re.M):
            req(rid in known_ids, f'{name}: unknown rule ID {rid}')

for m in re.finditer(r'`((?:references|templates|scripts)/[^`]+)`', text):
    rel = m.group(1)
    if '*' not in rel:
        req((ROOT / rel).exists(), f'SKILL.md references missing file: {rel}')

if errors:
    print('FAIL')
    for e in errors:
        print('-', e)
    sys.exit(1)

print('PASS')
print(f'canonical_rules={len(rules)}')
print('editorial_rules=R-DOC-013,R-DOC-014')
