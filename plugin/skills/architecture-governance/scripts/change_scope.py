#!/usr/bin/env python3
"""Read-only Git path-scope audit; does NOT decide architecture correctness."""
import argparse
import fnmatch
import json
from pathlib import Path
import subprocess
import sys


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", "replace").strip() or "git failed")
    return result.stdout


def changed_paths(repo, base):
    if not base or base.startswith("-"):
        raise ValueError("invalid base revision")
    git(repo, "rev-parse", "--verify", base + "^{commit}")
    tracked = git(repo, "diff", "--name-only", "--no-ext-diff", "-z", base, "--")
    untracked = git(repo, "ls-files", "--others", "--exclude-standard", "-z", "--")
    return sorted({
        name.decode("utf-8", "surrogateescape")
        for name in (tracked + untracked).split(b"\0") if name
    })


def checked_patterns(plan, key):
    value = plan.get(key, [])
    if not isinstance(value, list) or any(not isinstance(p, str) or not p for p in value):
        raise ValueError(f"{key} must be an array of nonempty glob strings")
    return value


def matches(path, patterns):
    # fnmatch wildcards may cross directory separators. Plans must be reviewed.
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def audit(repo, base, plan):
    allowed = checked_patterns(plan, "allowed_paths")
    protected = checked_patterns(plan, "protected_paths")
    changed = changed_paths(repo, base)
    unexpected = [p for p in changed if not matches(p, allowed)]
    blocked = [p for p in changed if matches(p, protected)]
    result = "FAIL" if blocked else "REVIEW_REQUIRED" if unexpected else "PASS"
    return {
        "result": result, "base": base, "changed_paths": changed,
        "unexpected_paths": unexpected, "protected_paths_changed": blocked,
        "proof_scope": "Git paths in HEAD-to-worktree diff plus untracked nonignored files",
        "does_not_prove": "semantic owner correctness, unstated dependencies, or tests passing"
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--base", default="HEAD")
    args = parser.parse_args(argv)
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
        if not isinstance(plan, dict):
            raise ValueError("plan must be a JSON object")
        result = audit(args.repo, args.base, plan)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return {"PASS": 0, "FAIL": 1, "REVIEW_REQUIRED": 2}[result["result"]]
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"result": "ERROR", "error": str(exc)}), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
