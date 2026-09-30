#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugin'
SKILL = PLUGIN / 'skills' / 'architecture-governance'
errors = []

def req(cond, msg):
    if not cond:
        errors.append(msg)

required = [
    ROOT / 'README.md',
    ROOT / 'README.ko.md',
    ROOT / 'doctrine' / 'ENGINEERING_CONSTITUTION.md',
    PLUGIN / '.claude-plugin' / 'plugin.json',
    SKILL / 'SKILL.md',
    SKILL / 'references' / 'rule-registry.json',
    SKILL / 'references' / 'engineering-constitution.md',
    SKILL / 'references' / 'editorial-policy.md',
]
for p in required:
    req(p.exists(), f'missing {p.relative_to(ROOT)}')

manifest_path = PLUGIN / '.claude-plugin' / 'plugin.json'
if manifest_path.exists():
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    req(manifest.get('name') == 'architecture-governance', 'manifest name mismatch')
    req(manifest.get('version') == '1.1.0', 'unexpected plugin version')

if (SKILL / 'references' / 'engineering-constitution.md').exists() and (ROOT / 'doctrine' / 'ENGINEERING_CONSTITUTION.md').exists():
    req((SKILL / 'references' / 'engineering-constitution.md').read_bytes() == (ROOT / 'doctrine' / 'ENGINEERING_CONSTITUTION.md').read_bytes(), 'doctrine projection differs from skill constitution')

validator = SKILL / 'scripts' / 'validate.py'
if validator.exists():
    proc = subprocess.run([sys.executable, str(validator)], cwd=SKILL, text=True, capture_output=True)
    if proc.returncode != 0:
        errors.append('skill validator failed:\n' + proc.stdout + proc.stderr)

if errors:
    print('FAIL')
    for e in errors:
        print('-', e)
    sys.exit(1)

print('PASS')
print('repository=Architecture-Governance')
print('version=1.1.0')
