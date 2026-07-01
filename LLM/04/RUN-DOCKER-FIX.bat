@echo off
:: Double-click: enables WSL2 + VM Platform (admin), then you must REBOOT.
powershell -NoProfile -Command "Start-Process powershell -Verb RunAs -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File \"\"E:\IT_SPACES\AI\ZoomCamp\LLM\04\fix-docker-wsl.ps1\"\"'"
pause
