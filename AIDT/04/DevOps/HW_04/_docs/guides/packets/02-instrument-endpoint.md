# Packet 02 — Instrument one endpoint / 엔드포인트 하나 계측 (Q2)

### 이 패킷의 역할
재미나이·학습자용 **소단계 입력**. Cursor는 이 패킷만 실행 범위로 삼는다. 끝나면 멈춘다.

### 출처
- Official: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/04-devops/homework.md — Question 2
- Starter: https://github.com/alexeygrigorev/order-tracker
- Packet 01 완료: `/healthz` → `{"status":"ok"}` (`AIDT_04_HW.md` Q1)

### 학습 목표
주문 조회(order lookup)에 OpenTelemetry **metrics / logs / traces**를 넣고, 콘솔로 내보낸 뒤 `docker compose logs app`에서 **요청 메트릭의 HTTP status**를 직접 보고 Q2에 답한다.

### 초보자가 할 일 (순서 고정)

1. Docker Desktop 엔진이 켜져 있는지 확인한다. `docker info`에 Server Version이 나와야 한다.
2. 앱 폴더로 이동:

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
Set-Location E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
```

3. 코딩 에이전트에게 아래 **Coding agent prompt**만 준다. (이 패킷 범위만. Collector/Grafana/알림은 아직.)
4. 에이전트 변경 후 재빌드:

```powershell
Set-Location E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
docker compose up --build -d --wait
```

8000이 쓰이면 Q1과 같이:

```powershell
$env:ORDER_TRACKER_PORT = "18080"
docker compose up --build -d --wait
```

그때 아래 URL·로그 명령의 포트도 맞춘다.

5. 주문 `standard-1001` 조회 (헤더 포함):

```powershell
curl.exe -i http://127.0.0.1:8000/api/orders/standard-1001
```

응답 **HTTP status 줄**과 본문을 눈으로 본다. (이것만으로 메트릭 status를 단정하지 말 것 — 메트릭은 로그에서 확인.)

6. 앱 로그에서 request metric 찾기:

```powershell
docker compose logs app --tail 200
```

로그에 route + HTTP status code가 붙은 **request metric** 줄을 찾는다.  
`Select-String`으로 좁히기 예:

```powershell
docker compose logs app --tail 300 | Select-String -Pattern "http|metric|status|orders|otel|Counter|histogram" -CaseSensitive:$false
```

7. 메트릭에 기록된 HTTP status code로 Q2를 고른다. 답을 `AIDT_04_HW.md` Q2 행에 적는다.

### Coding agent prompt
```text
In E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
add OpenTelemetry metrics, logs, and traces for order lookups
(GET /api/orders/{id} and related lookup path).

Requirements from Homework Q2:
- Request metric MUST include the route and the HTTP status code.
- Export signals to the console for now (so they appear in
  `docker compose logs app`).
- Do NOT add OpenTelemetry Collector, Prometheus, Loki, Tempo,
  or Grafana yet (that is Q3).
- Do NOT add Grafana alerts or incident-response (later questions).
- No AWS. This is Order Tracker, not Agent Relay.

After code changes, leave the learner to run:
  docker compose up --build -d --wait
Show which files you changed and how to spot the request metric
in console / compose logs. Do not invent the MCQ answer.
```

### Q2 선택지
Which HTTP status code does the metric record for this lookup?

- 200
- 301
- 404
- 500

정답은 **`docker compose logs app`에 찍힌 request metric**으로 고른다.  
curl 응답 줄만 보고 추측하지 말 것. 가이드/에이전트가 정답을 단정하지 말 것.

### 완료 기준
- [ ] OTel metrics + logs + traces가 order lookup에 들어감
- [ ] request metric에 route + HTTP status code 포함
- [ ] console export → `docker compose logs app`에서 보임
- [ ] `docker compose up --build -d --wait` 성공
- [ ] `curl.exe -i .../api/orders/standard-1001` 실행
- [ ] 로그에서 request metric의 status code를 직접 봄
- [ ] Q2 → `AIDT_04_HW.md`

### 하지 말 것
Collector / Prometheus / Loki / Tempo / Grafana 스택 추가, 알림, incident-response, Agent Relay 경로, AWS, Q3 미리 하기, git push(아직 제출 단계 아님).
다음 패킷(Packet 03 / Q3)은 허락 후.
