# Agent Relay — 터미널 전용 순차 스크립트 (01b)
# 전제: 다른 창에서 서버가 http://127.0.0.1:8000/ 에 떠 있음
# 대시보드 조작은 01b-dashboard-walkthrough.md 를 본다.
# 사용: 이 파일을 PowerShell에서 통째로 실행하거나, 블록 단위로 복사한다.

$ErrorActionPreference = "Stop"

cd E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1

# --- 헬스 체크 ---
Write-Host "`n[0] /health"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" | ConvertTo-Json

# --- alice 등록 ---
Write-Host "`n[1] alice 등록 — 응답의 agent_id / token 을 메모"
$alice = Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/agents" `
  -ContentType "application/json" `
  -Body '{"name":"alice"}'
$alice | ConvertTo-Json
Write-Host "alice.agent_id = $($alice.agent_id)"
Write-Host "alice.token    = $($alice.token)"
Write-Host ">> 지금 브라우저 Agent token 에 alice.token 붙여넣고 Use token 을 누른 뒤, Enter"
Read-Host

# --- bob 등록 ---
Write-Host "`n[2] bob 등록"
$bob = Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/agents" `
  -ContentType "application/json" `
  -Body '{"name":"bob"}'
$bob | ConvertTo-Json
Write-Host "bob.agent_id = $($bob.agent_id)"
Write-Host "bob.token    = $($bob.token)"
Write-Host ">> 대시보드에서 Refresh → Agents 에 alice/bob 보이는지 확인 후 Enter"
Read-Host

# --- 태스크 전송 (queued) ---
Write-Host "`n[3] alice → bob 태스크 전송 (status=queued 기대)"
$aliceHeaders = @{ Authorization = "Bearer $($alice.token)" }
$task = Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/tasks" `
  -Headers $aliceHeaders `
  -ContentType "application/json" `
  -Body (@{ to = $bob.agent_id; input = "hello packet02" } | ConvertTo-Json)
$task | ConvertTo-Json
Write-Host "task_id = $($task.task_id)  status = $($task.status)"
Write-Host ">> 대시보드 Refresh → My tasks Status=queued 확인 후 Enter"
Read-Host

# --- claim (processing) ---
Write-Host "`n[4] bob claim (claim_token 메모)"
$bobHeaders = @{ Authorization = "Bearer $($bob.token)" }
$claim = Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/tasks/claim" `
  -Headers $bobHeaders `
  -ContentType "application/json" `
  -Body '{"worker_id":"manual-ps1","wait_seconds":5}'
if (-not $claim) {
  throw "claim 응답이 비었습니다(HTTP 204). 태스크를 다시 보낸 뒤 재시도하세요."
}
$claim | ConvertTo-Json
Write-Host "claim.task_id     = $($claim.task_id)"
Write-Host "claim.claim_token = $($claim.claim_token)"
Write-Host ">> 대시보드 Refresh → Status=processing 확인 후 Enter"
Read-Host

# --- complete ---
Write-Host "`n[5] bob complete"
$completeBody = @{
  claim_token = $claim.claim_token
  output      = "HELLO PACKET02"
} | ConvertTo-Json
$done = Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/tasks/$($claim.task_id)/complete" `
  -Headers $bobHeaders `
  -ContentType "application/json" `
  -Body $completeBody
$done | ConvertTo-Json

# --- 보낸 사람(alice) 조회 ---
Write-Host "`n[6] alice GET task (status=completed, output 확인)"
$seen = Invoke-RestMethod -Method Get `
  -Uri "http://127.0.0.1:8000/api/v1/tasks/$($claim.task_id)" `
  -Headers $aliceHeaders
$seen | ConvertTo-Json
Write-Host "seen.status = $($seen.status)"
Write-Host "seen.output = $($seen.output)"
Write-Host ">> 대시보드 Refresh → Status=completed, Output / error = HELLO PACKET02 확인"
Write-Host "`n완료."
