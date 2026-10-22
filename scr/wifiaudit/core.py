"""Safe local inventory and reporting helpers."""
from __future__ import annotations

import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def run_command(args: list[str], timeout: int = 15) -> dict[str, Any]:
    """Run a fixed local diagnostic command and return structured output."""
    try:
        completed = subprocess.run(
            args, capture_output=True, text=True, timeout=timeout, check=False
        )
        return {
            "command": args,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"command": args, "error": str(exc)}


def wifi_inventory() -> dict[str, Any]:
    """Inventory nearby Wi-Fi networks via Windows netsh, if available."""
    data: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "task": "wifi_inventory",
    }
    if platform.system().lower() != "windows":
        data["available"] = False
        data["message"] = (
            "Windows netsh discovery is unavailable on this platform. "
            "Linux/macOS support requires a platform-specific adapter."
        )
        return data

    result = run_command(["netsh", "wlan", "show", "networks", "mode=bssid"])
    data["available"] = result.get("returncode") == 0
    data["raw_output"] = result.get("stdout", "")
    if result.get("error"):
        data["error"] = result["error"]
    if result.get("stderr"):
        data["stderr"] = result["stderr"]
    return data


def adapter_info() -> dict[str, Any]:
    """Report Windows WLAN capabilities without exporting credentials."""
    data: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": platform.platform(),
        "task": "adapter_info",
    }
    if platform.system().lower() != "windows":
        data["available"] = False
        data["message"] = "This adapter report currently uses Windows netsh."
        return data
    commands = {
        "interfaces": ["netsh", "wlan", "show", "interfaces"],
        "wireless_capabilities": ["netsh", "wlan", "show", "wirelesscapabilities"],
        "physical_adapters": [
            "powershell", "-NoProfile", "-Command",
            "Get-NetAdapter -Physical | Select-Object Name,InterfaceDescription,Status,LinkSpeed,MacAddress | ConvertTo-Json"
        ],
    }
    data["results"] = {name: run_command(cmd) for name, cmd in commands.items()}
    return data


def save_report(report: dict[str, Any], output_dir: str | Path = "reports") -> Path:
    """Save report to a timestamped JSON file."""
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = folder / f"{report.get('task', 'report')}_{stamp}.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return path
