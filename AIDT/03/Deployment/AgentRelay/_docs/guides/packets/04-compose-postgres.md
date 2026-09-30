# Packet 04 — Docker Compose and PostgreSQL / Compose+Postgres (Q4)

### 전제
Packet 03 완료.

### 출처
- homework.md Question 4

### 학습 목표
SQLite → PostgreSQL. `compose.yaml`에 앱 + 서비스 이름 `postgres`. 통합 테스트를 Compose 스택에 대해 통과시킨다.

### 초보자가 할 일
1. 에이전트에게 Postgres 전환 + `compose.yaml` 작성을 시킨다 (DB 서비스 이름 **`postgres`**).
2. `docker compose up --build` 실행 (E: 환경).
3. Q2 통합 테스트를 Compose에 대해 다시 돌리고 대시보드·DB 저장을 확인한다.
4. Q4 MCQ에 답한다.

### Coding agent prompt
```text
Replace SQLite with PostgreSQL and create a compose.yaml that runs Agent Relay
and PostgreSQL together. Name the database service postgres.
Show docker compose up --build and how to run the Q2 integration test against the stack.
Confirm data lands in Postgres. No kind/Kubernetes yet.
```

### Q4 선택지
Which hostname should the API use to connect to the `postgres` service in Docker Compose?
- `localhost`
- `postgres`
- `host.docker.internal`
- `0.0.0.0`

### 완료 기준
- [ ] `compose.yaml` + `docker compose up --build`
- [ ] 통합 테스트 통과 (Compose)
- [ ] Q4 → `AIDT_03_HW.md`

### 하지 말 것
kind, act CI.
