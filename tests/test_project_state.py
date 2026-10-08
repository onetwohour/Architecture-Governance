"""Adversarial tests of the source adapters and derived-state proof boundary."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
COMPILER = ROOT / "plugin/skills/architecture-governance/scripts/project_state.py"


def run(*args):
    return subprocess.run([sys.executable, str(COMPILER), *map(str, args)],
                          text=True, capture_output=True)


class ProjectStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email",
                        "test@example.invalid"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        docs = self.repo / "docs"
        (docs / "quality").mkdir(parents=True)
        (docs / "core.md").write_text("# Core\n")
        (docs / "architecture.toml").write_text(
            "[[document]]\nid = 'core'\npath = 'core.md'\ndepends_on = []\n"
        )
        (docs / "quality" / "probes.toml").write_text(
            "[[probe]]\nid = 'P-001'\nowners = ['core']\nrequired_before_stage = 1\n"
        )
        (docs / "quality" / "readiness.toml").write_text(
            "[[contract]]\nid = 'core.transaction'\nowner = 'core'\n"
            "state = 'PROBE_VALIDATED'\nmandatory_probes = ['P-001']\n"
            "evidence = ['src/probe.rs']\n"
        )
        (self.repo / "core-repo").mkdir()
        (self.repo / "core-repo" / "probe.rs").write_text("// probe: P-001\n")
        subprocess.run(["git", "-C", str(self.repo), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "baseline"], check=True)
        self.output = self.root / "generated"

    def command(self, *more):
        return run("--root", self.repo, "--adapter", "the-note", *more)

    def generated(self):
        return json.loads((self.output / "project-state.json").read_text())

    def test_declared_readiness_never_becomes_semantic_pass(self):
        result = self.command("--out", self.output, "--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        state = self.generated()
        self.assertEqual(state["probes"][0]["implementation"], "LOCATED")
        self.assertEqual(state["probes"][0]["execution"], "UNKNOWN")
        self.assertEqual(state["contracts"][0]["declared_readiness"], "PROBE_VALIDATED")
        self.assertEqual(state["contracts"][0]["execution_assessment"], "UNKNOWN")
        self.assertEqual(state["contracts"][0]["semantic_readiness"], "NOT_ASSESSED")

    def test_determinism_and_check(self):
        self.assertEqual(self.command("--out", self.output, "--write").returncode, 0)
        first = [(p.name, p.read_bytes()) for p in sorted(self.output.iterdir())]
        self.assertEqual(self.command("--out", self.output, "--check").returncode, 0)
        self.assertEqual(self.command("--out", self.output, "--write").returncode, 0)
        second = [(p.name, p.read_bytes()) for p in sorted(self.output.iterdir())]
        self.assertEqual(first, second)
        (self.output / "TODO.generated.md").write_text("manually edited\n")
        self.assertEqual(self.command("--out", self.output, "--check").returncode, 1)

    def test_unknown_owner_fails(self):
        p = self.repo / "docs" / "quality" / "probes.toml"
        p.write_text("[[probe]]\nid = 'P-001'\nowners = ['missing']\n")
        proc = self.command()
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unknown owner missing", proc.stderr)

    def test_unknown_contract_probe_fails(self):
        p = self.repo / "docs" / "quality" / "readiness.toml"
        p.write_text("[[contract]]\nid = 'core.transaction'\nowner = 'core'\n"
                     "mandatory_probes = ['P-999']\n")
        proc = self.command()
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unknown mandatory probe P-999", proc.stderr)

    def test_evidence_with_matching_revision_still_not_semantic_certification(self):
        head = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "HEAD"],
                              check=True, capture_output=True, text=True).stdout.strip()
        folder = self.root / "evidence"
        folder.mkdir()
        (folder / "probe.json").write_text(json.dumps({
            "label": "P-001", "result": "PASS", "exit_code": 0,
            "command_argv": ["python", "-m", "unittest"],
            "git_before": {"revision": head, "worktree_dirty": False},
            "git_after": {"revision": head, "worktree_dirty": False},
            "ended_at_utc": "2026-10-08T10:00:00Z"
        }))
        proc = self.command("--evidence-dir", folder, "--out", self.output, "--write")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        state = self.generated()
        self.assertEqual(state["probes"][0]["execution"], "COMMAND_PASS")
        self.assertEqual(state["contracts"][0]["execution_assessment"], "REVIEW_REQUIRED")
        self.assertEqual(state["contracts"][0]["semantic_readiness"], "NOT_ASSESSED")

    def test_dirty_worktree_makes_prior_pass_stale(self):
        head = subprocess.run(["git", "-C", str(self.repo), "rev-parse", "HEAD"],
                              check=True, capture_output=True, text=True).stdout.strip()
        folder = self.root / "evidence"
        folder.mkdir()
        (folder / "probe.json").write_text(json.dumps({
            "label": "P-001", "result": "PASS", "exit_code": 0,
            "command_argv": ["true"],
            "git_before": {"revision": head, "worktree_dirty": False},
            "git_after": {"revision": head, "worktree_dirty": False}
        }))
        (self.repo / "core-repo" / "probe.rs").write_text("// probe: P-001\n// edited\n")
        proc = self.command("--evidence-dir", folder, "--out", self.output, "--write")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(self.generated()["probes"][0]["execution"], "STALE")

    def test_open_issue_is_separate_from_probe(self):
        issue = self.root / "issues.toml"
        issue.write_text("[[issue]]\nid = 'SD-1'\nkind = 'SPEC_DEFECT'\n"
                         "state = 'OPEN'\nowner = 'core'\nsummary = 'Missing recovery law'\n"
                         "contracts = ['core.transaction']\n")
        proc = self.command("--issues", issue, "--out", self.output, "--write")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        state = self.generated()
        self.assertEqual(state["summary"]["open_issues"], 1)
        self.assertIn("SD-1", (self.output / "TODO.generated.md").read_text())

    def test_no_implicit_root_status_rewrite(self):
        (self.repo / "STATUS.md").write_text("MANUAL SOURCE\n")
        proc = self.command("--out", self.repo, "--write")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual((self.repo / "STATUS.md").read_text(), "MANUAL SOURCE\n")

    def test_duplicate_owner_fails(self):
        p = self.repo / "docs" / "architecture.toml"
        p.write_text("[[document]]\nid = 'core'\npath = 'core.md'\n"
                     "[[document]]\nid = 'core'\npath = 'core.md'\n")
        proc = self.command()
        self.assertEqual(proc.returncode, 2)
        self.assertIn("duplicate id core", proc.stderr)

    def test_cycle_in_owner_dependency_graph_is_rejected(self):
        arch = self.repo / "docs" / "architecture.toml"
        arch.write_text("[[document]]\nid = 'core'\npath = 'core.md'\n"
                        "depends_on = ['other']\n"
                        "[[document]]\nid = 'other'\npath = 'core.md'\n"
                        "depends_on = ['core']\n")
        proc = self.command()
        self.assertEqual(proc.returncode, 2)
        self.assertIn("owner dependency cycle", proc.stderr)

    def test_issue_markdown_does_not_insert_table_columns(self):
        issue = self.root / "issues.toml"
        issue.write_text("[[issue]]\nid = 'SD-1'\nkind = 'SPEC_DEFECT'\n"
                         "state = 'OPEN'\nowner = 'core'\n"
                         "summary = 'Two | incompatible meanings'\n")
        proc = self.command("--issues", issue, "--out", self.output, "--write")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("Two " + chr(92) + "| incompatible meanings",
                      (self.output / "TODO.generated.md").read_text())

    def test_normalized_json_no_project_specific_layout(self):
        snapshot = self.root / "snapshot.json"
        snapshot.write_text(json.dumps({
            "project": "generic",
            "owners": [{"id": "api", "depends_on": []}],
            "probes": [{"id": "P-100", "owners": ["api"]}],
            "contracts": [{"id": "api.schema", "owner": "api",
                           "mandatory_probes": ["P-100"], "declared_readiness": "DRAFT"}]
        }))
        proc = run("--root", self.repo, "--input", snapshot, "--out", self.output, "--write")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(self.generated()["project"], "generic")
        self.assertEqual(self.generated()["probes"][0]["implementation"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
