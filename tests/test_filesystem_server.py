import os
import sys
import unittest
from pathlib import Path

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
server_dir = os.path.join(repo_root, "server")
if server_dir not in sys.path:
    sys.path.insert(0, server_dir)

from config import MCP_SERVER_HOST, MCP_SERVER_PORT, WORKSPACE_DIR
from filesystem_mcp_server import validate_path


class TestFilesystemMCPServer(unittest.TestCase):
    def test_config_values(self):
        self.assertIsNotNone(MCP_SERVER_HOST)
        self.assertIsInstance(MCP_SERVER_PORT, int)
        self.assertTrue(WORKSPACE_DIR.exists())

    def test_path_traversal_prevention(self):
        # Absolute paths should be blocked
        with self.assertRaises(ValueError) as ctx:
            validate_path("C:/Windows/System32/calc.exe")
        self.assertIn("Absolute paths are not allowed", str(ctx.exception))

        # Traversal outside workspace should be blocked
        with self.assertRaises(ValueError) as ctx:
            validate_path("../../outside.txt")
        self.assertIn("Path traversal detected", str(ctx.exception))

    def test_valid_path_resolution(self):
        resolved = validate_path("sample.txt")
        self.assertEqual(resolved, (WORKSPACE_DIR / "sample.txt").resolve())


if __name__ == "__main__":
    unittest.main()
