import os
import sys
import types
import unittest


# Stub third-party modules so tests can import main.py without installing deps.
aiohttp_stub = types.ModuleType("aiohttp")
aiohttp_stub.ClientSession = object
sys.modules.setdefault("aiohttp", aiohttp_stub)

notion_client_stub = types.ModuleType("notion_client")

class _DummyAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

notion_client_stub.AsyncClient = _DummyAsyncClient
sys.modules.setdefault("notion_client", notion_client_stub)

# Prevent interactive prompt on import for legacy code path.
os.environ.setdefault("NOTION_TOKEN", "test-notion-token")

import main  # noqa: E402


class TestConfigLoading(unittest.TestCase):
    def test_load_config_requires_notion_token_and_database_id(self):
        env = {}
        with self.assertRaises(ValueError):
            main.load_config_from_env(env)

    def test_load_config_accepts_env_values(self):
        env = {
            "NOTION_TOKEN": "notion_xxx",
            "GITHUB_TOKEN": "ghp_xxx",
            "DATABASE_ID": "db_123",
        }
        cfg = main.load_config_from_env(env)
        self.assertEqual(cfg["notion_token"], "notion_xxx")
        self.assertEqual(cfg["github_token"], "ghp_xxx")
        self.assertEqual(cfg["database_id"], "db_123")


if __name__ == "__main__":
    unittest.main()
