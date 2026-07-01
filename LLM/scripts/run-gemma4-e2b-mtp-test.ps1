# Gemma 4 E2B + MTP smoke test (PowerShell; llama-cli lacks --spec-type).
$ErrorActionPreference = "Stop"

$Root = "E:\IT_SPACES\AI\ZoomCamp\LLM"
$Server = Join-Path $Root "atomic-llama-cpp-turboquant\build\bin\llama-server.exe"
$ModelDir = Join-Path $Root "models\gemma-4-e2b"
$Main = if ($env:MAIN_GGUF) { $env:MAIN_GGUF } else { Join-Path $ModelDir "gemma-4-E2B-it-Q4_K_M.gguf" }
$Draft = if ($env:DRAFT_GGUF) { $env:DRAFT_GGUF } else { Join-Path $ModelDir "gemma-4-E2B-it-assistant.Q4_K_M.gguf" }
$Prompt = if ($env:PROMPT) { $env:PROMPT } else { "hello" }
$NPredict = if ($env:N_PREDICT) { [int]$env:N_PREDICT } else { 32 }
$Ctx = if ($env:CTX) { [int]$env:CTX } else { 4096 }
$HostAddr = if ($env:HOST) { $env:HOST } else { "127.0.0.1" }
$Port = if ($env:PORT) { [int]$env:PORT } else { 8081 }

if (-not (Test-Path $Server)) { throw "llama-server not found: $Server" }
if (-not (Test-Path $Main)) { throw "target GGUF not found: $Main" }
if (-not (Test-Path $Draft)) { throw "assistant GGUF not found: $Draft" }

Write-Host "=== Gemma 4 E2B MTP smoke test (CPU) ==="
Write-Host "MAIN:  $Main"
Write-Host "DRAFT: $Draft"
Write-Host "PROMPT: $Prompt"
Write-Host ""

$serverArgs = @(
  "-m", $Main,
  "--mtp-head", $Draft,
  "--spec-type", "mtp",
  "--draft-block-size", "2",
  "--draft-max", "6",
  "-c", "$Ctx",
  "-ngl", "0",
  "-ngld", "0",
  "-ctk", "turbo3",
  "-ctv", "turbo3",
  "-ctkd", "turbo3",
  "-ctvd", "turbo3",
  "--host", $HostAddr,
  "--port", "$Port",
  "--parallel", "1",
  "-np", "1",
  "--cont-batching",
  "--no-warmup"
)

$proc = Start-Process -FilePath $Server -ArgumentList $serverArgs -PassThru -NoNewWindow
try {
  $ready = $false
  for ($i = 0; $i -lt 120; $i++) {
    try {
      Invoke-WebRequest -Uri "http://${HostAddr}:${Port}/health" -UseBasicParsing -TimeoutSec 2 | Out-Null
      $ready = $true
      break
    } catch {
      Start-Sleep -Seconds 2
    }
  }
  if (-not $ready) { throw "server did not become ready on port $Port" }

  Write-Host "=== completion ==="
  $body = @{ prompt = $Prompt; n_predict = $NPredict; temperature = 0 } | ConvertTo-Json -Compress
  $resp = Invoke-RestMethod -Uri "http://${HostAddr}:${Port}/completion" -Method Post -ContentType "application/json" -Body $body
  $resp | ConvertTo-Json -Depth 6
  Write-Host ""
  Write-Host "=== done ==="
} finally {
  if (-not $proc.HasExited) {
    Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
  }
}
