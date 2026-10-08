#!/usr/bin/env python3
"""Execute a real command and capture bounded, revision-specific evidence."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


MAX_LOG = 32768


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", "replace") or "Git unavailable")
    return result.stdout.decode("utf-8", "replace").strip()


def snapshot(repo):
    return {
        "revision": git(repo, "rev-parse", "HEAD"),
        "worktree_dirty": bool(git(repo, "status", "--porcelain=v1", "--untracked-files=all")),
    }


def execute(repo, command, label, timeout):
    before = snapshot(repo)
    began = datetime.now(timezone.utc).isoformat()
    try:
        result = subprocess.run(command, cwd=repo, capture_output=True, text=True,
                                errors="replace", timeout=timeout, shell=False)
        exit_code = result.returncode
        stdout, stderr = result.stdout, result.stderr
        failure = None
    except subprocess.TimeoutExpired as exc:
        exit_code = 124
        stdout = exc.stdout or b""
        stderr = exc.stderr or b""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", "replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "replace")
        failure = "TIMEOUT"
    except OSError as exc:
        exit_code = 127
        stdout, stderr, failure = "", "", str(exc)
    ended = datetime.now(timezone.utc).isoformat()
    after = snapshot(repo)
    stale = before["revision"] != after["revision"]
    return {
        "schema_version": 1,
        "label": label, "command_argv": command, "cwd": str(repo),
        "started_at_utc": began, "ended_at_utc": ended,
        "platform": platform.platform(), "python": platform.python_version(),
        "git_before": before, "git_after": after,
        "result": "STALE" if stale else "PASS" if exit_code == 0 else "FAIL",
        "exit_code": exit_code, "failure": failure,
        "stdout_tail": stdout[-MAX_LOG:], "stderr_tail": stderr[-MAX_LOG:],
        "proof_scope": "Observed exit status of exactly this command on this worktree",
        "does_not_prove": "semantic correctness, missing negative cases, CI readiness",
        "clean_worktree_at_execution": bool(not before["worktree_dirty"]
                                            and not after["worktree_dirty"])
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--label", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--timeout", type=float, default=600)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command or args.timeout <= 0:
        parser.error("provide -- <executable> [args...] and a positive timeout")
    repo = args.repo.resolve()
    try:
        record = execute(repo, command, args.label, args.timeout)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
        print(f'{record["result"]}: {args.label}; evidence={args.output}')
        return 0 if record["result"] == "PASS" else 1
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: evidence collection failed: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
