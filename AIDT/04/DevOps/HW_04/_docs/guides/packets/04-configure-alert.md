# Packet 04 — Configure the alert / 알림 설정 (Q4)

### 이 패킷의 역할
재미나이·학습자용 **소단계 입력**. Cursor는 이 패킷만 실행 범위로 삼는다. 끝나면 멈춘다.

### 출처
- Official: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/04-devops/homework.md — Question 4
- Starter: https://github.com/alexeygrigorev/order-tracker
- Packet 03 완료: pipeline + Grafana → `standard-1002` metric `404` (`AIDT_04_HW.md` Q3)

### 학습 목표
Grafana에 **5xx** 응답을 감시하는 alert를 넣고, `standard-1002` lookup을 다시 날린 뒤 Grafana가 보여주는 **alert state**를 직접 보고 Q4에 답한다. (webhook·responder 연결은 Q6.)

### 초보자가 할 일 (순서 고정)

1. Docker Desktop 엔진이 켜져 있는지 확인한다. `docker info`에 Server Version이 나와야 한다.
2. 앱 폴더로 이동:

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
Set-Location E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
```

3. 코딩 에이전트에게 아래 **Coding agent prompt**만 준다. (이 패킷 범위만. responder·webhook은 아직.)
4. 에이전트 변경 후 스택 반영:

```powershell
Set-Location E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
docker compose up --build -d --wait
```

8000이 쓰이면:

```powershell
$env:ORDER_TRACKER_PORT = "18080"
docker compose up --build -d --wait
```

5. Q3와 같은 lookup을 다시 실행:

```powershell
curl.exe -i http://127.0.0.1:8000/api/orders/standard-1002
```

(`ORDER_TRACKER_PORT`를 썼으면 URL 포트를 맞춘다.)

6. Grafana에서 alert 상태를 본다 (보통 `http://127.0.0.1:3000` → Alerting / 해당 alert rule).  
   평가가 끝날 때까지 잠시 기다린다 (수 초~1분).

7. Grafana가 보여주는 state로 Q4를 고른다. 답을 `AIDT_04_HW.md` Q4 행에 적는다.

### Coding agent prompt
```text
In E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
add a Grafana alert for Homework Q4 (5xx responses).

Requirements from Homework Q4:
- Add a Grafana alert that watches the 5xx request metric
  (order lookup / HTTP 5xx).
- Include in the alert: the endpoint, the time window, and a
  dashboard link.
- Handle periods with no 5xx responses (do not leave the rule
  stuck in a misleading No data state if the homework expects
  a proper "no errors" handling — e.g. or vector(0) / nodata
  handling as appropriate for Grafana unified alerting).
- Enable Grafana unified alerting as needed for the rule to work.
- Save alert config in the repository (provisioning YAML/JSON).
- Do NOT connect webhook to incident-response yet (Q6).
- Do NOT build the responder / headless agent (Q5–Q6).
- No AWS. This is Order Tracker, not Agent Relay.

After changes, leave the learner to run:
  docker compose up --build -d --wait
  curl.exe -i http://127.0.0.1:8000/api/orders/standard-1002
Show: Grafana URL, where to open the alert rule / state,
and how long to wait for evaluation.
Do not invent the MCQ answer (Normal / Firing / Pending / No data).
```

### Q4 선택지
What state does Grafana show?

- Normal
- Firing
- Pending
- No data

정답은 **Grafana alert UI에 보이는 state**로 고른다.  
curl 응답(404 등)만 보고 추측하지 말 것. 가이드/에이전트가 정답을 단정하지 말 것.  
참고: Q3의 `standard-1002`는 **404**(클라이언트/미존재)이지 **5xx**(서버 오류)가 아니다. alert는 5xx를 본다.

### 완료 기준
- [ ] Grafana 5xx alert가 저장소에 있음 (provisioning)
- [ ] alert에 endpoint · time window · dashboard link 포함
- [ ] 5xx 없는 구간 처리됨
- [ ] `docker compose up --build -d --wait` 성공
- [ ] `curl.exe -i .../api/orders/standard-1002` 재실행
- [ ] Grafana에서 alert state를 직접 봄
- [ ] Q4 → `AIDT_04_HW.md`

### 하지 말 것
webhook → responder 연결, incident-response 서비스 빌드, headless agent, Agent Relay 경로, AWS, Q5+ 미리 하기, git push(아직 제출 단계 아님), alert state 추측해서 폼에 적기.
다음 패킷(Packet 05 / Q5)은 허락 후.
