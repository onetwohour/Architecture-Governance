"""Executable negative tests for the governance helper proof boundaries."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugin" / "skills" / "architecture-governance" / "scripts"


def invoke(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout


class GovernanceRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "test@example.invalid")
        git(self.repo, "config", "user.name", "Test")
        (self.repo / "src.py").write_text("original\n")
        git(self.repo, "add", "src.py")
        git(self.repo, "commit", "-qm", "initial")
        self.plan = self.root / "plan.json"

    def scope(self, allowed, protected=()):
        self.plan.write_text(json.dumps({
            "allowed_paths": list(allowed), "protected_paths": list(protected)
        }))
        result = invoke(SCRIPTS / "change_scope.py", "--repo", self.repo,
                        "--plan", self.plan)
        return result, json.loads(result.stdout) if result.stdout else None

    def test_clean_pass(self):
        result, report = self.scope(["src.py"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report["result"], "PASS")

    def test_untracked_paths_are_not_hidden(self):
        (self.repo / "new.txt").write_text("new\n")
        result, report = self.scope(["src.py"])
        self.assertEqual(result.returncode, 2)
        self.assertEqual(report["unexpected_paths"], ["new.txt"])

    def test_protected_file_never_passes(self):
        (self.repo / "STATUS.md").write_text("do not edit\n")
        result, report = self.scope(["**"], ["STATUS.md"])
        self.assertEqual(result.returncode, 1)
        self.assertEqual(report["protected_paths_changed"], ["STATUS.md"])

    def test_git_diff_includes_staged_and_unstaged(self):
        (self.repo / "src.py").write_text("staged\n")
        git(self.repo, "add", "src.py")
        (self.repo / "src.py").write_text("unstaged\n")
        result, report = self.scope(["elsewhere/**"])
        self.assertEqual(result.returncode, 2)
        self.assertIn("src.py", report["unexpected_paths"])

    def test_validation_pass_with_real_execution(self):
        out = self.root / "pass.json"
        result = invoke(SCRIPTS / "run_validation.py", "--repo", self.repo,
                        "--label", "unit", "--output", out, "--",
                        sys.executable, "-c", "print('ok')")
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads(out.read_text())
        self.assertEqual(evidence["result"], "PASS")
        self.assertEqual(evidence["exit_code"], 0)
        self.assertTrue(evidence["reusable_for_clean_commit"])

    def test_validation_fail_is_never_pass(self):
        out = self.root / "fail.json"
        result = invoke(SCRIPTS / "run_validation.py", "--repo", self.repo,
                        "--label", "negative", "--output", out, "--",
                        sys.executable, "-c", "raise SystemExit(7)")
        self.assertEqual(result.returncode, 1, result.stderr)
        evidence = json.loads(out.read_text())
        self.assertEqual(evidence["result"], "FAIL")
        self.assertEqual(evidence["exit_code"], 7)

    def test_dirty_worktree_pass_is_not_reusable(self):
        (self.repo / "new.txt").write_text("changed\n")
        out = self.root / "dirty.json"
        result = invoke(SCRIPTS / "run_validation.py", "--repo", self.repo,
                        "--label", "dirty", "--output", out, "--",
                        sys.executable, "-c", "pass")
        self.assertEqual(result.returncode, 0)
        evidence = json.loads(out.read_text())
        self.assertEqual(evidence["result"], "PASS")
        self.assertFalse(evidence["reusable_for_clean_commit"])

    def test_no_command_is_rejected(self):
        out = self.root / "missing.json"
        result = invoke(SCRIPTS / "run_validation.py", "--repo", self.repo,
                        "--label", "missing", "--output", out)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
