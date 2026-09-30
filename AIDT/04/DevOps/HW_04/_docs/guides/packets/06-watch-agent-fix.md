# Packet 06 — Watch the agent fix the incident / 에이전트가 사고 고치기 (Q6)

### 이 패킷의 역할
재미나이·학습자용 **소단계 입력**. Cursor는 이 패킷만 실행 범위로 삼는다. 끝나면 멈춘다.

### 출처
- Official: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/04-devops/homework.md — Question 6
- Starter: https://github.com/alexeygrigorev/order-tracker
- Packet 05 완료: responder `:8001` + ResponderTest → last line `Test alert handled successfully; standing down.` (`AIDT_04_HW.md` Q5)

### 학습 목표
Grafana 5xx alert를 responder webhook에 연결한 뒤, `express-1002` lookup으로 실제 알림을 유발하고, headless 에이전트가 고친 뒤 같은 요청이 더 이상 문제를 내지 않는지 확인한다. **무엇이 문제였는지** MCQ로 답한다.

### 초보자가 할 일 (순서 고정)

1. Docker Desktop 엔진이 켜져 있는지 확인한다. 앱 + 텔레메트리 스택 + responder(:8001)가 떠 있어야 한다.
2. 앱 폴더로 이동:

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
Set-Location E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
```

3. 코딩 에이전트에게 아래 **Coding agent prompt**만 준다. (이 패킷: webhook 연결 + 실제 사고 흐름. 제출용 push는 학습자가 마지막에.)
4. 에이전트 변경 후 스택·responder 반영 (에이전트가 안내한 compose / Grafana recreate / responder 재기동).
5. 문제 요청:

```powershell
curl.exe -i http://127.0.0.1:8000/api/orders/express-1002
```

알림이 안 뜨면 **여러 번** 반복한다. Grafana alert state가 Firing으로 가는지, webhook이 `POST http://127.0.0.1:8001/alerts`로 가는지 본다.

6. headless 에이전트가 끝날 때까지 기다린다. 응답·evidence·코드 변경을 확인한다.
7. 앱을 재시작한 뒤 같은 curl을 다시 실행해, 문제가 재현되지 않는지 확인한다.
8. MCQ로 Q6을 고른다. 답을 `AIDT_04_HW.md` Q6 행에 적는다. (가이드/에이전트가 선택지를 단정하지 말 것 — 직접 본 원인으로.)

### Coding agent prompt
```text
In E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
complete Homework Q6 (real Grafana alert → webhook → responder → fix).

Requirements from Homework Q6:
- Connect the existing Grafana 5xx alert to the incident responder
  via a webhook contact point → POST http://host.docker.internal:8001/alerts
  (or the correct URL so Grafana-in-Docker can reach the responder on the host).
  Save contact point / notification policy provisioning in the repo.
- Keep evidence collection + headless coding assistant on alert (from Q5).
  For real (non-test) alerts, the assistant should investigate and apply a
  minimal fix. Prefer Cursor CLI `agent -p` when CURSOR_API_KEY / login works;
  document how the learner authenticates if needed.
- Do NOT invent the Q6 MCQ answer. Leave the learner to observe the fix
  and choose among the four official options.
- No AWS. Order Tracker only (not Agent Relay).

After changes, leave the learner to:
  1) ensure app + telemetry + Grafana + responder(:8001) are up
  2) curl.exe -i http://127.0.0.1:8000/api/orders/express-1002
     (repeat if alert does not fire)
  3) watch webhook → /alerts and headless fix
  4) restart app and re-curl express-1002 to verify recovery
  5) answer the MCQ from what they observed
Show Grafana webhook config location, where to watch alert/webhook,
where the agent response and code fix land.
```

### Q6 선택지
What was the problem?

- The express delivery date calculation tried to use a day that does not exist in that month.
- The order timestamp could not be parsed because it had no time zone.
- The app rejected the order's `preparing` status.
- The lookup searched the wrong database column for express orders.

정답은 **재현·수정·검증 뒤에 본 원인**으로 고른다. 가이드가 미리 찍어주지 말 것.

### 완료 기준
- [ ] Grafana 5xx alert → webhook → responder `:8001/alerts`
- [ ] `curl.exe -i .../express-1002`로 알림 유발 (필요 시 반복)
- [ ] webhook 수신 + headless 조사/수정 관찰
- [ ] 앱 재시작 후 같은 요청이 더 이상 문제 없음
- [ ] Q6 → `AIDT_04_HW.md`
- [ ] (제출 시) commit/push telemetry, alert, responder, evidence, fix — 학습자가 폼에 repo URL

### 하지 말 것
MCQ 추측으로 폼에 적기, AWS Create stack, Agent Relay 초안을 제출로 쓰기, Q5 테스트 알림만으로 Q6을 끝냈다고 하기.
다음 패킷 없음 — HW4 공식 문제 끝. 제출은 학습자.
