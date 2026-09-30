# Packet 03 — Build the telemetry pipeline / 텔레메트리 파이프라인 (Q3)

### 이 패킷의 역할
재미나이·학습자용 **소단계 입력**. Cursor는 이 패킷만 실행 범위로 삼는다. 끝나면 멈춘다.

### 출처
- Official: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/04-devops/homework.md — Question 3
- Starter: https://github.com/alexeygrigorev/order-tracker
- Packet 02 완료: console export → `order_lookup_requests` + `http.status_code=200` for `standard-1001` (`AIDT_04_HW.md` Q2)

### 학습 목표
앱 텔레메트리를 **Collector → Prometheus / Loki / Tempo → Grafana**로 보내고, Grafana에서 `standard-1002` lookup의 **request metric HTTP status**를 직접 본 뒤 Q3에 답한다. 로그·트레이스도 같이 보이는지 확인한다.

### 초보자가 할 일 (순서 고정)

1. Docker Desktop 엔진이 켜져 있는지 확인한다. `docker info`에 Server Version이 나와야 한다.
2. 앱 폴더로 이동:

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
Set-Location E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
```

3. 코딩 에이전트에게 아래 **Coding agent prompt**만 준다. (이 패킷 범위만. Grafana 알림·responder는 아직.)
4. 에이전트 변경 후 재빌드:

```powershell
Set-Location E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
docker compose up --build -d --wait
```

8000이 쓰이면 Q1/Q2와 같이:

```powershell
$env:ORDER_TRACKER_PORT = "18080"
docker compose up --build -d --wait
```

포트 충돌(3000 / 9090 / 4317 / 4318 등)이 나면 에이전트가 compose에 쓴 포트로 Grafana·Collector에 접속한다. 볼륨·데이터는 **E:** 쪽만 (C:\Users 금지).

5. 주문 `standard-1002` 조회 (헤더 포함):

```powershell
curl.exe -i http://127.0.0.1:8000/api/orders/standard-1002
```

(`ORDER_TRACKER_PORT`를 썼으면 URL 포트를 맞춘다.)

응답 HTTP status 줄과 본문을 눈으로 본다. **최종 Q3 답은 Grafana의 request metric**에서 고른다 (curl만으로 단정하지 말 것).

6. Grafana를 연다 (보통 `http://127.0.0.1:3000` — compose에 다른 포트면 그걸 쓴다).  
   에이전트가 만든 **request counts / errors** 대시보드에서 이번 lookup의 request metric을 찾는다.  
   같은 lookup의 **log**와 **trace**도 Grafana(또는 연결된 Loki/Tempo)에서 보이는지 확인한다.

7. 메트릭에 기록된 HTTP status code로 Q3를 고른다. 답을 `AIDT_04_HW.md` Q3 행에 적는다.

### Coding agent prompt
```text
In E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
extend the stack for Homework Q3 (telemetry pipeline).

Requirements from Homework Q3:
- Add OpenTelemetry Collector, Prometheus, Loki, Tempo, and Grafana
  to Docker Compose (same repo; config files saved in the repository).
- Send the app's metrics, logs, and traces through the Collector
  (replace or supplement Q2 console-only export as needed so signals
  reach the pipeline; keep request metric with route + HTTP status code).
- Create a Grafana dashboard for request counts and errors.
- Bind mounts / named volumes for telemetry data must live on E:
  (e.g. under E:/IT_SPACES/AI/ZoomCamp/AIDT/04/DevOps/order-tracker/…).
  Do NOT put data under C:\Users\...
- Prefer localhost binds. If ports 3000/9090/4317/4318 conflict,
  document the alternate ports clearly for the learner.
- Do NOT add Grafana 5xx alerts yet (Q4).
- Do NOT build incident-response / webhook / headless agent (Q5–Q6).
- No AWS. This is Order Tracker, not Agent Relay.

After code/config changes, leave the learner to run:
  docker compose up --build -d --wait
  curl.exe -i http://127.0.0.1:8000/api/orders/standard-1002
Show: Grafana URL/login if any, which dashboard panel to open,
and how to confirm metric + log + trace for that lookup.
Do not invent the MCQ answer (404/200/301/500).
```

### Q3 선택지
Which HTTP status code does the metric show?

- 404
- 200
- 301
- 500

정답은 **Grafana에 보이는 request metric**으로 고른다.  
curl 응답 줄만 보고 추측하지 말 것. 가이드/에이전트가 정답을 단정하지 말 것.  
로그·트레이스도 “보인다”만 확인하면 됨 (답 선택지는 status code만).

### 완료 기준
- [ ] Collector + Prometheus + Loki + Tempo + Grafana가 Compose에 있음
- [ ] 설정 파일이 저장소에 커밋 가능한 형태로 있음
- [ ] 앱 시그널이 Collector를 거쳐 저장소로 감
- [ ] Grafana에 request counts / errors 대시보드 있음
- [ ] `docker compose up --build -d --wait` 성공
- [ ] `curl.exe -i .../api/orders/standard-1002` 실행
- [ ] Grafana에서 해당 lookup의 request metric status를 직접 봄
- [ ] 같은 lookup의 log·trace도 확인함
- [ ] Q3 → `AIDT_04_HW.md`

### 하지 말 것
Grafana 5xx 알림, incident-response, webhook, headless agent, Agent Relay 경로, AWS Create stack, Q4+ 미리 하기, git push(아직 제출 단계 아님), 메트릭 status를 추측해서 폼에 적기.
다음 패킷(Packet 04 / Q4)은 허락 후.
