# Packet 01 — Run the app / 앱 실행 (Q1)

### 이 패킷의 역할
재미나이·학습자용 **소단계 입력**. Cursor는 이 패킷만 실행 범위로 삼는다. 끝나면 멈춘다.

### 출처
- Official: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/04-devops/homework.md — Question 1
- Starter (fork): https://github.com/alexeygrigorev/order-tracker
- README: docker compose, `/healthz`, three sample orders on first start

### 학습 목표
Order Tracker를 Compose로 띄우고, **직접** health 응답 JSON을 본 뒤 Q1에 답한다.

### 초보자가 할 일 (순서 고정)

1. Docker Desktop 엔진이 켜져 있는지 본다. `Docker Engine stopped`면 Restart/Start + UAC. `docker info`에 Server Version이 나와야 한다.
2. GitHub에서 https://github.com/alexeygrigorev/order-tracker 를 **본인 계정으로 Fork**.
3. Fork를 여기로 클론한다 (아직 없으면 Cursor/학습자가 클론):

```powershell
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
Set-Location E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps
git clone https://github.com/zakard114/order-tracker.git order-tracker
Set-Location .\order-tracker
```

이미 `order-tracker\`가 있으면 clone 하지 말고 그 폴더로 들어간다.

4. 앱 시작:

```powershell
Set-Location E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
docker compose up --build -d --wait
```

8000이 쓰이면:

```powershell
$env:ORDER_TRACKER_PORT = "18080"
docker compose up --build -d --wait
```

그때 health URL의 포트도 18080으로 바꾼다.

5. 브라우저로 `http://127.0.0.1:8000/` 을 연다 (페이지가 보여야 한다).
6. health:

```powershell
curl.exe http://127.0.0.1:8000/healthz
```

**화면에 찍힌 JSON을 그대로 본다.** 추측으로 고르지 말 것.
7. Q1 답을 `AIDT_04_HW.md`에 적는다.

### Coding agent prompt
```text
Read the Order Tracker README. On Windows, from
E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker
run docker compose up --build -d --wait if Docker Engine is up.
Then curl.exe http://127.0.0.1:8000/healthz and show the exact body.
Do not add OpenTelemetry yet. Do not touch AWS.
```

### Q1 선택지
What does the health check return?

- `{"status":"ok"}`
- `{"status":"error"}`
- `{"orders":3}`
- `pong`

정답은 curl 출력으로 고른다. README는 `/healthz`가 DB health check라고만 한다.

### 완료 기준
- [ ] Fork 존재
- [ ] 클론 경로가 E: DevOps\order-tracker
- [ ] compose up 성공
- [ ] curl 본문을 직접 봄
- [ ] Q1 → `AIDT_04_HW.md`

### 하지 말 것
OpenTelemetry, Grafana, 알림, incident-response, Agent Relay 계측, AWS, git push (아직 숙제 커밋 단계 아님).
다음 패킷(Q2)은 허락 후.
