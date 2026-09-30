# Packet 05 — Build the automatic responder / 자동 리스폰더 (Q5)

### 이 패킷의 역할
재미나이·학습자용 **소단계 입력**. Cursor는 이 패킷만 실행 범위로 삼는다. 끝나면 멈춘다.

### 출처
- Official: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/04-devops/homework.md — Question 5
- Starter: https://github.com/alexeygrigorev/order-tracker
- Packet 04 완료: Grafana 5xx alert → state **Normal** after `standard-1002` (`AIDT_04_HW.md` Q4)

### 학습 목표
`incident-response/`에 Grafana 알림을 받는 서비스(`POST /alerts`, port **8001**)를 만들고, 알림 시 evidence 저장 + coding assistant를 **headless**로 띄운다. 테스트 알림을 보낸 뒤 **에이전트 응답(마지막 줄 포함)** 을 직접 읽고 Q5에 적는다.

### 초보자가 할 일 (순서 고정)

1. Docker Desktop 엔진이 켜져 있는지 확인한다. (앱·텔레메트리 스택은 Packet 03/04와 같이 떠 있으면 됨.)
2. 앱/레포 폴더로 이동:

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
Set-Location E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
```

3. 코딩 에이전트에게 아래 **Coding agent prompt**만 준다. (이 패킷 범위만. Grafana webhook 연결·express-1002 실사고는 Q6.)
4. 에이전트가 리스폰더를 준비한 뒤, 안내한 방식으로 리스폰더를 기동한다. (Compose 서비스 또는 로컬 프로세스 — 에이전트가 문서화한 명령을 쓴다.) 포트는 **8001**.
5. 테스트 알림 전송:

```powershell
curl.exe -X POST http://127.0.0.1:8001/alerts `
  -H "Content-Type: application/json" `
  -d "{\"alerts\":[{\"status\":\"firing\",\"labels\":{\"alertname\":\"ResponderTest\",\"test\":\"true\"},\"annotations\":{\"summary\":\"Test notification; no incident to fix\"}}]}"
```

6. 에이전트(headless)가 끝날 때까지 기다린다. 응답이 저장된 파일/로그를 에이전트 안내에 따라 연다.
7. **에이전트가 답한 내용**을 읽고, **마지막 줄**을 포함해 Q5에 적는다. `AIDT_04_HW.md` Q5 행.

### Coding agent prompt
```text
In E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
build the automatic incident responder for Homework Q5.

Requirements from Homework Q5:
- Service under incident-response/ that receives Grafana alerts at
  POST /alerts on port 8001.
- When an alert arrives, save information needed to understand the
  problem (e.g. affected endpoint, logs, traces) into the repo
  (evidence under incident-response/, E: paths only — no C:\Users).
- On alert, start the coding assistant automatically in headless mode.
  Prefer Cursor CLI / agent headless if available on this machine;
  document the exact command and how the learner reads the response.
  For labels.test=true / "no incident to fix" test alerts, the agent
  should still produce a readable response (not invent a fake production fix).
- Do NOT wire Grafana webhook contact point yet (that is Q6).
- Do NOT require the learner to hit express-1002 for this question (Q6).
- No AWS. This is Order Tracker, not Agent Relay draft paths.

After implementation, leave the learner to:
  1) start the responder on :8001
  2) run the official test curl to POST /alerts (ResponderTest)
  3) wait and read the agent response (include last line for the form)
Show start command, where the response is written, and how long to wait.
Do not invent the free-text Q5 answer.
```

### Q5 답 형식
객관식 아님. 폼 질문:

> What did the agent respond? Include the last line from its answer.

정답은 **실제로 저장된 에이전트 응답**에서 가져온다. 가이드/에이전트가 문구를 지어내지 말 것.

### 완료 기준
- [ ] `incident-response/` 서비스: `POST /alerts` on `:8001`
- [ ] 알림 시 evidence 저장 (endpoint / logs / traces 등)
- [ ] 알림 시 coding assistant headless 기동
- [ ] 리스폰더 기동 성공
- [ ] 공식 테스트 curl (`ResponderTest`) 실행
- [ ] 에이전트 응답을 직접 읽음 (마지막 줄 포함)
- [ ] Q5 → `AIDT_04_HW.md`

### 하지 말 것
Grafana webhook 연결, `express-1002` 실사고 유발(Q6), Agent Relay 초안 경로를 제출용으로 쓰기, AWS, Q6 미리 하기, 에이전트 응답을 추측해서 폼에 적기.
다음 패킷(Packet 06 / Q6)은 허락 후.
