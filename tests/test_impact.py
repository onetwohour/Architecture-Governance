"""Reverse dependency traversal is advisory and must be deterministic."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
IMPACT = ROOT / "plugin/skills/architecture-governance/scripts/impact.py"


class ImpactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.snapshot = self.path / "snapshot.json"
        self.snapshot.write_text(json.dumps({
            "owners": [
                {"id": "core", "depends_on": []},
                {"id": "editor", "depends_on": ["core"]},
                {"id": "ui", "depends_on": ["editor"]},
                {"id": "independent", "depends_on": []}
            ],
            "probes": [
                {"id": "P-001", "owners": ["core"]},
                {"id": "P-002", "owners": ["ui"]},
                {"id": "P-003", "owners": ["independent"]}
            ],
            "contracts": [
                {"id": "c1", "owner": "editor", "mandatory_probes": ["P-002"]},
                {"id": "c2", "owner": "independent", "mandatory_probes": ["P-003"]}
            ]
        }))

    def invoke(self, *args):
        return subprocess.run([sys.executable, str(IMPACT), "--root", str(self.path),
                               "--input", str(self.snapshot), *args],
                              capture_output=True, text=True)

    def test_transitive_dependents_and_related_probes(self):
        proc = self.invoke("--owner", "core")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["affected_owners"], ["core", "editor", "ui"])
        self.assertEqual(result["candidate_probes"], ["P-001", "P-002"])
        self.assertEqual(result["candidate_contracts"], ["c1"])
        self.assertIn("does_not_prove", result)

    def test_unrelated_owner_stays_out_of_set(self):
        proc = self.invoke("--owner", "independent")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result["affected_owners"], ["independent"])
        self.assertEqual(result["candidate_probes"], ["P-003"])

    def test_unknown_owner_fails_closed(self):
        proc = self.invoke("--owner", "typo")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unknown owner(s)", proc.stderr)

    def test_broken_dependency_is_a_compiler_error(self):
        obj = json.loads(self.snapshot.read_text())
        obj["owners"][0]["depends_on"] = ["missing"]
        self.snapshot.write_text(json.dumps(obj))
        proc = self.invoke("--owner", "core")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unknown dependency", proc.stderr)


if __name__ == "__main__":
    unittest.main()
