# WiFi Audit Tool

A small, modular, open-source starter project for **authorized Wi-Fi security auditing**.
It focuses on local Wi-Fi inventory, adapter capability reporting, and safe checks of
systems you own or are explicitly authorized to assess.

## Features

- List nearby Wi-Fi networks using Windows `netsh`
- Report physical network adapters and available WLAN capabilities
- Show current WLAN interface and saved profile names (never exports passwords)
- Optional TCP reachability checks for a specified authorized host
- Save timestamped JSON reports
- PowerShell entry point and Python package layout for future cross-platform modules

## Requirements

- Windows 10/11 for the current PowerShell Wi-Fi discovery commands
- PowerShell 5.1+; Python 3.10+ for the modular CLI
- Git to clone the repository

## Run with PowerShell

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\wifi-audit.ps1
```

## Run with Python

```powershell
python -m venv .venv
# Windows:
.venv\Scripts\Activate.ps1
# Linux/macOS:
# source .venv/bin/activate

python -m pip install -e .
wifi-audit
```

The Python CLI provides a portable project entry point; Wi-Fi discovery currently uses
Windows `netsh` where available. Linux support for monitor-mode capture depends on
compatible hardware, drivers, permissions, and distro packages, so it is not assumed.

## Reports

Reports are written to `reports/`. Generated reports are ignored by Git.

## Scope and safety

Use only on networks and devices you own or have explicit permission to test. This project
does not forcibly disconnect clients, harvest authentication material, crack Wi-Fi
passwords, or bypass access controls. A missing response does not prove a host is offline.

## Development

```powershell
python -m pip install -e ".[dev]"
pytest
```

## License

MIT. See `LICENSE`.
