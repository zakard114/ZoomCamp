# 초보자 가이드: 대시보드 화면 분석 및 실전 따라하기

> 대상: Windows PowerShell + 브라우저 초보  
> UI 소스: `dashboard.html` (버튼·라벨 이름 **그대로**)  
> 서버: `http://127.0.0.1:8000/`  
> 명령만 모은 스크립트: [`01b-commands-only.ps1`](./01b-commands-only.ps1)

로컬에서 서버를 띄우고 브라우저로 접속했을 때 마주하는 그 화면이 바로 Agent Relay의 메인 제어탑(대시보드)입니다.

여기에 왜 접속했고, 화면에 나오는 것들은 무슨 의미이며, 터미널과 어떻게 연동해서 에이전트들의 움직임을 관찰하는지 — 초보자의 눈높이에 맞춰 처음부터 끝까지 차근차근 짚어 봅니다.

중간에서 “등록은 알아서” 같은 생략은 없습니다. 터미널 블록은 **그대로 복사해 붙여넣으면** 됩니다.  
**중요:** PowerShell 변수(`$alice`, `$bob`, `$claim` …)는 **같은 터미널 창**에서 끝까지 이어 가야 합니다.

---

## 1. 지금 대시보드 화면에서 내가 보고 있는 것은 무엇인가요?

**웹 화면의 실제 구성:** 커다란 ‘등록 버튼’이나 ‘태스크 보내기 버튼’은 **없습니다.**  
있는 것은 이것뿐입니다.

| 종류 | 화면에 보이는 이름 |
|------|-------------------|
| 입력란 | **Agent token** |
| 버튼 (상단) | **Use token**, **Clear** |
| 버튼 (**Agents** 섹션 옆) | **Refresh** |
| 데이터 영역(섹션) | **Agents**, **My tasks** |

**이 화면의 진짜 정체:** 에이전트들이 일하고 있는 상태를 눈으로 확인하는 **관찰용 창문(Dashboard)** 입니다.  
실제로 에이전트를 등록하고 태스크를 주고받는 일은 **API / PowerShell** 로 하고, 브라우저는 Bearer 토큰으로 **읽기만** 합니다.

토큰은 브라우저 **`sessionStorage`** (`relay-token`)에만 잠깐 둡니다. 탭을 닫으면 사라집니다. (`localStorage`가 아닙니다.)

상태 lifecycle: `queued` → `processing` → `completed`  
(`delivered` 같은 상태는 **없습니다.**)

> **타이밍 주의:** claim과 complete를 **한 블록**에 붙여넣으면, 그다음 Refresh 때는 이미 `completed`라서 **`processing`을 못 볼 수 있습니다.**  
> 아래 ④에서는 claim → **Refresh(`processing`)** → complete → **Refresh(`completed`)** 순서를 **반드시** 지킵니다.

---

## 0) 준비 (터미널 A — 서버)

PowerShell을 하나 엽니다.

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
uv sync
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

확인:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
```

기대: `{ "status": "ok" }`

이 터미널은 **끄지 말고** 둡니다. 아래부터는 **다른 PowerShell 창(터미널 B)** 에서 합니다.  
서버가 이미 `8000`에 떠 있으면 **0)을 생략**해도 됩니다.

---

## 2. 순서대로 따라 해보기 (실행 시나리오)

브라우저에서 `http://127.0.0.1:8000/` 를 연 뒤, 대시보드와 터미널(PowerShell)을 함께 활용합니다.

### ① 토큰 없이 새로고침 해보기 (인증 확인)

상단의 **Agent token** 칸을 비워 둔 채 **Refresh**를 누릅니다.

화면에 아래 에러 문구가 뜨는 것이 **정상**입니다. (브라우저가 임의로 일을 처리하지 않고 인증을 거친다는 증거입니다.)

```text
Authorization: Bearer <agent-token> is required.
```

(드물게 네트워크/파싱 실패 시 `Request failed` 도 가능 — 그래도 “토큰 없이 읽기 실패”면 의미는 같습니다.)

---

### ② 에이전트 등록하기 (터미널 활용)

**새 터미널 창(터미널 B)** 을 켜고 프로젝트 경로로 이동한 뒤, 아래를 **통째로** 붙여넣습니다.  
alice와 bob이 등록되면서 각각의 고유 토큰이 발급됩니다. (`token`은 **이 응답에만** 나오므로 반드시 메모합니다.)

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1

$alice = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/agents" `
  -ContentType "application/json" -Body '{"name":"alice"}'
Write-Host "alice.token = $($alice.token)"

$bob = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/agents" `
  -ContentType "application/json" -Body '{"name":"bob"}'
Write-Host "bob.agent_id = $($bob.agent_id)"; Write-Host "bob.token = $($bob.token)"
```

| 필드 | 의미 | 다음에 쓰는 곳 |
|------|------|----------------|
| `alice.token` | alice 비밀 토큰 (`agt_…`) | 대시보드 **Agent token**, 태스크 전송 |
| `bob.agent_id` | bob ID | `POST /tasks` 의 `to` |
| `bob.token` | bob 비밀 토큰 (`agt_…`) | claim / complete |

---

### ③ 대시보드에 토큰 적용하기

1. 터미널에 출력된 **alice.token** 값을 복사합니다.
2. 웹 대시보드 상단 **Agent token** 칸에 붙여넣고 **Use token**을 누릅니다.
3. 상태 줄에 `Updated` + 시각이 뜨면 OK. 이제 브라우저는 **alice** 권한으로 목록을 봅니다.
4. **Refresh**를 한 번 더 눌러도 됩니다. **Agents** 표에 **alice**, **bob** 행이 보이면 OK.

---

### ④ 태스크 주고받기 및 상태 관찰 (단계별 진행)

#### [1단계] 태스크 보내기 (터미널)

**같은 터미널 B**에서 alice가 bob에게 일감을 던집니다.

```powershell
$aliceHeaders = @{ Authorization = "Bearer $($alice.token)" }
$task = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/tasks" `
  -Headers $aliceHeaders -ContentType "application/json" `
  -Body (@{ to = $bob.agent_id; input = "hello packet02" } | ConvertTo-Json)
$task
```

**대시보드 확인 ①:** **Refresh** → **My tasks** 에서 Status가 **`queued`**(대기 중)로 나타납니다.

| 열 | 기대 |
|----|------|
| `Status` | **`queued`** |
| `Input` | `hello packet02` |
| `Route` | alice → bob 형태 |

---

#### [2단계] bob이 일감 가져오기 / Claim (터미널)

```powershell
$bobHeaders = @{ Authorization = "Bearer $($bob.token)" }
$claim = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/tasks/claim" `
  -Headers $bobHeaders -ContentType "application/json" `
  -Body '{"worker_id":"manual-ps1","wait_seconds":5}'
$claim
```

가져올 일이 없으면 서버는 **HTTP 204**(본문 없음)를 돌려줍니다.  
PowerShell에서는 `$claim`이 **빈 문자열**처럼 보이거나 출력이 비어 있습니다.

> 결과가 **비어 있거나** 204라면 **complete로 넘어가지 말고 멈춥니다.**  
> (`-not $claim` 이면 7) 전송을 다시 한 뒤 claim을 재실행합니다.)  
> 204인데 complete까지 이어 붙이면 `$claim.task_id`가 비어 URL이 깨집니다.

성공 시 `$claim`에 `task_id`, `claim_token`, `input` 등이 보입니다.

**대시보드 확인 ②:** 이 시점에서 **Refresh**를 누르면 Status가 **`processing`**(처리 중)으로 바뀐 것을 **명확히** 볼 수 있습니다.  
← **이 단계를 건너뛰지 마세요.** (claim+complete를 한 번에 붙이면 이 화면을 놓칩니다.)

---

#### [3단계] bob이 처리 완료 보고하기 / Complete (터미널)

```powershell
Invoke-RestMethod -Method Post `
  -Uri "http://127.0.0.1:8000/api/v1/tasks/$($claim.task_id)/complete" `
  -Headers $bobHeaders -ContentType "application/json" `
  -Body (@{ claim_token = $claim.claim_token; output = "HELLO PACKET02" } | ConvertTo-Json)
```

응답의 `status`가 **`completed`** 이면 OK.

---

#### [4단계] 최종 상태 검증 및 Q2 연동 (터미널)

alice 권한으로 태스크가 잘 끝났는지 조회합니다. (`$aliceHeaders`, `$claim.task_id` 사용)

```powershell
Invoke-RestMethod -Method Get `
  -Uri "http://127.0.0.1:8000/api/v1/tasks/$($claim.task_id)" `
  -Headers $aliceHeaders   # status = completed (Q2 정답 검증)
```

기대: `status` = **`completed`**, `output` = `HELLO PACKET02`  
(선택지 `delivered` 는 없습니다.)

**대시보드 확인 ③:** 마지막으로 **Refresh** → Status가 **`completed`**(완료), **Output / error**에 `HELLO PACKET02` 가 보이면 전체 플로우 끝입니다.

---

## 14) Clear / 다시 로그인 (선택)

1. **Clear** 클릭 → 칸·표·메시지가 비워짐 (`sessionStorage`의 `relay-token`도 삭제)
2. alice 토큰 다시 붙여넣기 → **Use token**
3. **Refresh** 로 목록만 다시 불러오기

---

## (선택) worker CLI로 claim+complete 한 번에

수동 ②~④ 대신 README 워커를 쓸 수 있습니다. **별도 터미널**에서:

```powershell
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1

uv run python main.py worker `
  --base-url http://127.0.0.1:8000 `
  --name uppercase `
  --credentials ./uppercase-credentials.json `
  --worker-id laptop-1
```

그다음 alice를 API로 등록하고, 워커 `agent_id`(credentials JSON 또는 **Agents** 표)로 `POST /tasks` 하면 워커가 `input.upper()` 후 complete 합니다.  
끝나면 대시보드에 alice 토큰으로 **Use token** → **Refresh**.

---

## 3. 이 화면을 볼 때의 핵심 관전 포인트 (아키텍처)

이 과정을 직접 밟아 보며 “아, 이래서 Q1의 정답이 그거였구나!” 하고 고정하면 됩니다.

**관전 포인트 ①: 브라우저는 일을 직접 하지 않는다**  
Refresh 할 때마다 목록이 바뀌어도, 브라우저가 작업을 계산·저장하는 게 아닙니다. 서버(DB) 상태를 **보여주는 창문**일 뿐입니다.

**관전 포인트 ②: 에이전트들은 서로 직접 대화하지 않는다 (P2P가 아님)**  
alice가 bob에게 파일을 직접 던지지 않습니다. alice는 **중앙 Relay(DB)** 에 일을 올려두고, bob은 HTTP로 **claim** 해서 가져갑니다.

**관전 포인트 ③: HTTP API와 DB의 숨은 공로**  
등록 → DB 저장 → claim → 결과 제출이 전부 HTTP API와 SQLite 큐 위에서 돕니다. 메시지 브로커는 없습니다.

**Which description matches the project's architecture?**

- [ ] Agents exchange tasks directly with each other.  
  → 아님. Relay(API+DB)를 통한다.
- [x] Agents claim tasks from a DB through an HTTP API.  
  → **정답.** claim도 HTTP, 저장도 DB.
- [ ] Agents consume tasks from a message broker.  
  → 아님. 브로커 없음. SQLite 큐.
- [ ] The browser stores and executes tasks.  
  → 아님. 브라우저는 **보기만** (`sessionStorage`에 토큰만).

---

## 한 줄 체크리스트

- [ ] `/` 에서 **Agent token** / **Use token** / **Clear** / **Agents** / **Refresh** / **My tasks** 확인
- [ ] 토큰 없이 **Refresh** → `Authorization: Bearer <agent-token> is required.` 확인
- [ ] PowerShell로 alice·bob 등록 → 토큰을 **Agent token**에 넣고 **Use token**
- [ ] 태스크 `queued` → (**Refresh**) claim 후 `processing` → complete 후 `completed` 를 **단계마다 Refresh**로 확인
- [ ] alice `GET /tasks/{id}` 에서 `status=completed`, `output` 확인 (Q2)
- [ ] Q1·Q2 답을 `AIDT_03_HW.md`에 기록

---

## 대시보드만으로는 못 하는 일

| 하고 싶은 일 | 대시보드 | 어디서 |
|-------------|----------|--------|
| 에이전트 등록 | ❌ | `POST /api/v1/agents` (②) |
| 태스크 보내기 | ❌ | `POST /api/v1/tasks` (④-1) |
| claim / complete | ❌ | claim·complete API (④-2·3) |
| 목록·상태 보기 | ✅ | **Use token** / **Refresh** |
