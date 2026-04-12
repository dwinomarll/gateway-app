#!/usr/bin/env python3
"""GATEWAY CLI — start / install / uninstall / status / release"""
import argparse, shutil, subprocess, sys, urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
VENV_PYTHON = ROOT / ".venv" / "bin" / "python"
PLIST_SRC = ROOT / "launchagents" / "ai.gateway.core.plist"
PLIST_DST = Path.home() / "Library" / "LaunchAgents" / "ai.gateway.core.plist"

def cmd_start():
    subprocess.run([str(VENV_PYTHON), "-m", "uvicorn", "backend.server:app",
        "--host", "127.0.0.1", "--port", "9191", "--reload"], cwd=ROOT)

def cmd_install():
    content = PLIST_SRC.read_text().replace("GATEWAY_ROOT_PLACEHOLDER", str(ROOT)).replace("VENV_PYTHON_PLACEHOLDER", str(VENV_PYTHON))
    PLIST_DST.parent.mkdir(parents=True, exist_ok=True)
    PLIST_DST.write_text(content)
    subprocess.run(["launchctl", "load", str(PLIST_DST)], check=True)
    print(f"✅ LaunchAgent installed: {PLIST_DST}")

def cmd_uninstall():
    if PLIST_DST.exists():
        subprocess.run(["launchctl", "unload", str(PLIST_DST)])
        PLIST_DST.unlink()
        print("✅ LaunchAgent removed.")
    else:
        print("LaunchAgent not installed.")

def cmd_status():
    try:
        with urllib.request.urlopen("http://localhost:9191/health", timeout=3) as r:
            print(f"✅ GATEWAY running — {r.read().decode()}")
    except Exception:
        print("❌ GATEWAY not responding on localhost:9191")

def cmd_release():
    today = datetime.now().strftime("%Y.%-m.%-d")
    tag = f"v{today}"
    log = subprocess.run(["git", "log", "--oneline", "-20"], capture_output=True, text=True, cwd=ROOT).stdout
    entry = f"## {tag}\n{log}\n\n"
    clog = ROOT / "CHANGELOG.md"
    clog.write_text(entry + (clog.read_text() if clog.exists() else ""))
    subprocess.run(["git", "add", "CHANGELOG.md"], cwd=ROOT)
    subprocess.run(["git", "commit", "-m", f"chore: changelog {tag}"], cwd=ROOT)
    subprocess.run(["git", "tag", tag], cwd=ROOT)
    subprocess.run(["git", "push", "origin", "main", "--tags"], cwd=ROOT)
    subprocess.run(["gh", "release", "create", tag, "--title", f"GATEWAY {tag}", "--notes", entry], cwd=ROOT)
    print(f"✅ Released {tag}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GATEWAY CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    for c in ["start", "install", "uninstall", "status", "release"]:
        sub.add_parser(c)
    args = parser.parse_args()
    {"start": cmd_start, "install": cmd_install, "uninstall": cmd_uninstall, "status": cmd_status, "release": cmd_release}[args.cmd]()
