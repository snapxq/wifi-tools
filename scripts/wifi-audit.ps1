# Windows PowerShell entry point for WiFi Audit Tool
$ErrorActionPreference = "Continue"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Reports = Join-Path $ProjectRoot "reports"
New-Item -ItemType Directory -Force $Reports | Out-Null

function Save-Report($Name, $Data) {
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $path = Join-Path $Reports "${Name}_${stamp}.json"
    $Data | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $path
    Write-Host "`n[+] Report saved: $path" -ForegroundColor Green
}

function Show-Discovery {
    $raw = netsh wlan show networks mode=bssid
    $report = [pscustomobject]@{
        Timestamp = (Get-Date).ToString("o")
        Task = "wifi_discovery"
        RawOutput = ($raw -join "`n")
        Note = "Windows WLAN output depends on adapter and driver capabilities."
    }
    $raw
    Save-Report "wifi_discovery" $report
}

function Show-AdapterInfo {
    Write-Host "`n--- WLAN Interfaces ---" -ForegroundColor Cyan
    $interfaces = netsh wlan show interfaces
    $interfaces
    Write-Host "`n--- Wireless Capabilities ---" -ForegroundColor Cyan
    $capabilities = netsh wlan show wirelesscapabilities
    $capabilities
    $adapters = Get-NetAdapter -Physical -ErrorAction SilentlyContinue |
        Select-Object Name, InterfaceDescription, Status, LinkSpeed, MacAddress
    $adapters | Format-Table -AutoSize
    Save-Report "adapter_info" ([pscustomobject]@{
        Timestamp = (Get-Date).ToString("o")
        Task = "adapter_info"
        Interfaces = ($interfaces -join "`n")
        Capabilities = ($capabilities -join "`n")
        PhysicalAdapters = @($adapters)
    })
}

do {
    Clear-Host
    Write-Host "===================================="
    Write-Host "          WiFi Audit Tool"
    Write-Host "===================================="
    Write-Host "1. Discover nearby Wi-Fi networks"
    Write-Host "2. Inspect Wi-Fi adapter and capabilities"
    Write-Host "3. Open reports folder"
    Write-Host "0. Exit"
    $choice = Read-Host "Select"
    switch ($choice) {
        "1" { Show-Discovery; Pause }
        "2" { Show-AdapterInfo; Pause }
        "3" { Invoke-Item $Reports }
        "0" { break }
        default { Write-Host "Unknown option."; Start-Sleep -Seconds 1 }
    }
} while ($choice -ne "0")
