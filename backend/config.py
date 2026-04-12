"""GATEWAY Core — Configuration"""
import os, json, subprocess
from pathlib import Path

NOTION_API_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"
MY4_NOTES_DB = "2106ae29-a07c-81dd-a782-c482d020c533"

_notion_token: str | None = None

def get_notion_token() -> str:
    global _notion_token
    if _notion_token:
        return _notion_token
    token = os.environ.get("NOTION_API_TOKEN")
    if token:
        _notion_token = token
        return _notion_token
    result = subprocess.run(
        ["security", "find-generic-password", "-s", "NOTION_API_TOKEN", "-w"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        _notion_token = result.stdout.strip()
        return _notion_token
    raise RuntimeError("NOTION_API_TOKEN not found in env or keychain")

OPENCLAW_URL = "http://localhost:18790"
_openclaw_token: str | None = None

def get_openclaw_token() -> str:
    global _openclaw_token
    if _openclaw_token:
        return _openclaw_token
    config_path = Path.home() / ".openclaw" / "openclaw.json"
    config = json.loads(config_path.read_text())
    _openclaw_token = config["gateway"]["auth"]["token"]
    return _openclaw_token

N8N_URL = "https://n8n.srv1299016.hstgr.cloud"
SHIFT4_STATUS_URL = "https://shift4internalalerts.statuspage.io/"
GATEWAY_HOST = "127.0.0.1"
GATEWAY_PORT = 9191
HEALTH_POLL_INTERVAL = 60
