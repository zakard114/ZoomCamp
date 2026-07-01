# Start Gemma 4 E2B + MTP llama-server (background). Stop: Stop-Process -Name llama-server -Force
$ErrorActionPreference = "Stop"
$Root = "E:\IT_SPACES\AI\ZoomCamp\LLM"
$Server = Join-Path $Root "atomic-llama-cpp-turboquant\build\bin\llama-server.exe"
$Main = Join-Path $Root "models\gemma-4-e2b\gemma-4-E2B-it-Q4_K_M.gguf"
$Draft = Join-Path $Root "models\gemma-4-e2b\gemma-4-E2B-it-assistant.Q4_K_M.gguf"
$Port = if ($env:PORT) { [int]$env:PORT } else { 8081 }

if (Get-Process -Name "llama-server" -ErrorAction SilentlyContinue) {
  Write-Host "llama-server already running"
  exit 0
}

$args = @(
  "-m", $Main,
  "--mtp-head", $Draft,
  "--spec-type", "mtp",
  "--draft-block-size", "2",
  "--draft-max", "6",
  "-c", "4096",
  "-ngl", "0", "-ngld", "0",
  "-ctk", "turbo3", "-ctv", "turbo3", "-ctkd", "turbo3", "-ctvd", "turbo3",
  "--host", "127.0.0.1", "--port", "$Port",
  "--parallel", "1", "-np", "1",
  "--cont-batching"
)

Write-Host "Starting llama-server on http://127.0.0.1:$Port ..."
Start-Process -FilePath $Server -ArgumentList $args -WindowStyle Minimized
for ($i = 0; $i -lt 120; $i++) {
  try {
    Invoke-WebRequest -Uri "http://127.0.0.1:$Port/health" -UseBasicParsing -TimeoutSec 2 | Out-Null
    Write-Host "Ready."
    exit 0
  } catch { Start-Sleep -Seconds 2 }
}
throw "Server did not become ready within 4 minutes"
