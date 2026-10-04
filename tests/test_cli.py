import unittest

from gary.cli import build_status, repo_root


class CliTests(unittest.TestCase):
    def test_project_root_contains_spec(self):
        self.assertTrue((repo_root() / "PROJECT_SPEC.md").exists())

    def test_status_has_core_fields(self):
        data = build_status()
        self.assertIn("health", data)
        self.assertIn("installation_level", data)
        self.assertIn("host", data)
        self.assertIn("capabilities", data["host"])
