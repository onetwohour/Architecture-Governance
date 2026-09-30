#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT.parents[1]
errors=[]

def req(cond,msg):
    if not cond: errors.append(msg)

# Skill frontmatter
skill = ROOT/'SKILL.md'
req(skill.exists(), 'SKILL.md missing')
text = skill.read_text(encoding='utf-8') if skill.exists() else ''
req(text.startswith('---\n'), 'SKILL.md must start with YAML frontmatter')
req(re.search(r'^name:\s*architecture-governance\s*$', text, re.M), 'skill name mismatch')
req(re.search(r'^description:\s*.+$', text, re.M), 'skill description missing')

# Claude Code plugin manifest
cman = PLUGIN_ROOT/'.claude-plugin'/'plugin.json'
req(cman.exists(), '.claude-plugin/plugin.json missing')
if cman.exists():
    m=json.loads(cman.read_text(encoding='utf-8'))
    req(m.get('$schema')=='https://json.schemastore.org/claude-code-plugin-manifest.json','Claude plugin schema mismatch')
    req(m.get('name')=='architecture-governance','plugin name mismatch')
    req(m.get('displayName')=='Architecture Governance','display name mismatch')
    req(bool(m.get('version')),'plugin version missing')
    req(m.get('repository')=='https://github.com/onetwohour/Architecture-Governance','repository metadata mismatch')

# Registry
regp=ROOT/'references'/'rule-registry.json'
req(regp.exists(),'rule-registry.json missing')
if regp.exists():
    reg=json.loads(regp.read_text(encoding='utf-8'))
    rules=reg.get('rules',[])
    ids=[r.get('id') for r in rules]
    req(len(rules)>=1,'no canonical rules')
    req(len(ids)==len(set(ids)),'duplicate rule IDs')
    allowed_p={'CORE','CONDITIONAL','PROFILE'}
    allowed_s={'MUST','SHOULD','DEFAULT'}
    for r in rules:
        for k in ['id','title','category','statement','rationale','portability','strength','enforcement']:
            req(bool(r.get(k)),f"{r.get('id','?')}: missing {k}")
        req(r.get('portability') in allowed_p,f"{r.get('id')}: invalid portability")
        req(r.get('strength') in allowed_s,f"{r.get('id')}: invalid strength")
        if r.get('portability')=='CONDITIONAL':
            req(bool(r.get('applies_when')),f"{r.get('id')}: conditional rule missing applies_when")

# All relative files referenced by SKILL.md must exist.
for m in re.finditer(r'`((?:references|templates|scripts)/[^`]+)`', text):
    rel=m.group(1)
    if '*' in rel:
        base = rel.split('*',1)[0].rstrip('/')
        req((ROOT/base).exists(), f'SKILL.md references missing directory: {base}')
    else:
        req((ROOT/rel).exists(), f'SKILL.md references missing file: {rel}')

# Positional section references are forbidden inside policy prose, excluding the policy that describes the ban itself.
for p in [ROOT/'references'/'decision-policy.md', ROOT/'references'/'architecture-policy.md', ROOT/'references'/'evidence-policy.md']:
    if p.exists():
        t=p.read_text(encoding='utf-8')
        req('§' not in t, f'{p.name}: contains positional section marker')

if errors:
    print('FAIL')
    for e in errors: print('-',e)
    sys.exit(1)
print('PASS')
print(f'plugin_root={PLUGIN_ROOT}')
print(f'canonical_rules={len(json.loads(regp.read_text(encoding="utf-8"))["rules"])}')
