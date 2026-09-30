# Packet 03 — Containerization / 컨테이너화 (Q3)

### 전제
Packet 02 완료 (통합 테스트 있음).

### 출처
- homework.md Question 3
- Official tip: uvicorn `--host 0.0.0.0` inside the container

### 학습 목표
`Dockerfile`로 `agent-relay:local` 이미지를 만들고, 포트를 호스트에 공개한 채 Q2 흐름을 컨테이너에서 재현한다.

### 초보자가 할 일
1. 에이전트에게 Dockerfile 작성·빌드·실행을 맡긴다 (이미지 이름 고정: `agent-relay:local`).
2. **필수:** 컨테이너 안 uvicorn은 `--host 0.0.0.0` (기본 `127.0.0.1`이면 `-p`가 안 되는 것처럼 보임).
3. 대시보드로 Q2 태스크 흐름을 **컨테이너 API**에 대해 반복한다.
4. Q3 MCQ에 답한다.

### Coding agent prompt
```text
Create a Dockerfile for Agent Relay. Build the image as agent-relay:local
and run it with the API port published to the host.
Run uvicorn with --host 0.0.0.0 inside the container (required; default 127.0.0.1 breaks -p).
Keep using E: caches where relevant. Show the exact docker build/run commands for Windows PowerShell.
Do not add Compose or Kubernetes yet.
```

### Q3 선택지
Which Docker option publishes a container's port to your machine?
- `--expose`
- `-p`
- `-v`
- `--name`

### 완료 기준
- [ ] `agent-relay:local` 빌드·실행 (`0.0.0.0` bind)
- [ ] 컨테이너 상대로 태스크 흐름 확인
- [ ] Q3 → `AIDT_03_HW.md`

### 하지 말 것
Compose Postgres, kind, CI.
