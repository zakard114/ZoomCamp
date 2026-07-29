# Fix Docker Desktop "HCS_E_HYPERV_NOT_INSTALLED" / WSL2 not supported
# MUST run as Administrator (right-click PowerShell -> Run as administrator)
#Requires -RunAsAdministrator

$ErrorActionPreference = "Stop"

Write-Host "=== Docker / WSL2 fix (Windows 11 Pro) ===" -ForegroundColor Cyan

$features = @(
    "Microsoft-Windows-Subsystem-Linux",
    "VirtualMachinePlatform"
)

foreach ($name in $features) {
    $feat = Get-WindowsOptionalFeature -Online -FeatureName $name
    Write-Host "$name : $($feat.State)"
    if ($feat.State -ne "Enabled") {
        Write-Host "  -> Enabling (may take a few minutes)..."
        Enable-WindowsOptionalFeature -Online -FeatureName $name -All -NoRestart | Out-Null
        Write-Host "  -> Enabled." -ForegroundColor Green
    }
}

# Ensure hypervisor starts at boot (needed for WSL2 VMs)
$hypervisor = bcdedit /enum "{current}" 2>&1 | Select-String "hypervisorlaunchtype"
Write-Host "`nBoot config: $hypervisor"
if ($hypervisor -notmatch "auto|on") {
    Write-Host "Setting hypervisorlaunchtype auto..."
    bcdedit /set hypervisorlaunchtype auto | Out-Null
}

Write-Host "`nShutting down WSL..."
wsl --shutdown 2>$null

Write-Host "Updating WSL kernel..."
wsl --update

Write-Host "Default WSL version -> 2"
wsl --set-default-version 2

Write-Host "`n=== Verification ===" -ForegroundColor Cyan
Write-Host "BIOS virtualization (should be True):"
(Get-CimInstance Win32_Processor).VirtualizationFirmwareEnabled
Write-Host "Hypervisor present (True after reboot):"
(Get-CimInstance Win32_ComputerSystem).HypervisorPresent

wsl --status
wsl -l -v

Write-Host "`n*** REBOOT the PC, then start Docker Desktop. ***" -ForegroundColor Yellow
Write-Host "If Docker still fails: Docker Desktop -> Settings -> General -> uncheck 'Use the WSL 2 based engine' is WRONG - keep WSL2 ON."
Write-Host "Module 04 (2025 RAG) without Docker: use Anaconda kernel + Ollama only (Elasticsearch/Qdrant need Docker after fix)."
