"""Command-line entry point."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import adapter_info, save_report, wifi_inventory


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="wifi-audit",
        description="Wi-Fi inventory and defensive audit helper",
    )
    parser.add_argument(
        "action",
        choices=["discover", "adapter-info"],
        help="Diagnostic action to run",
    )
    parser.add_argument(
        "--reports-dir",
        default="reports",
        help="Directory for JSON reports (default: reports)",
    )
    args = parser.parse_args()

    report = wifi_inventory() if args.action == "discover" else adapter_info()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    path = save_report(report, Path(args.reports_dir))
    print(f"\n[+] Report saved to: {path}")


if __name__ == "__main__":
    main()
