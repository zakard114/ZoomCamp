# Read-only check (no admin). Run: .\fix-docker-wsl-check.ps1

Write-Host "OS:" (Get-CimInstance Win32_OperatingSystem).Caption
Write-Host "BIOS virtualization enabled:" (Get-CimInstance Win32_Processor).VirtualizationFirmwareEnabled
Write-Host "Hypervisor running now:" (Get-CimInstance Win32_ComputerSystem).HypervisorPresent
Write-Host ""
Write-Host "WSL:"
wsl --status 2>&1
wsl -l -v 2>&1
Write-Host ""
Write-Host "If HypervisorPresent is False -> run fix-docker-wsl.ps1 AS ADMIN, then REBOOT."
