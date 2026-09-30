# Packet 01 — Understand the project / 프로젝트 이해하기 (Q1)

### 이 패킷의 역할
재미나이·학습자용 **소단계 입력**. Cursor는 이 패킷만 실행 범위로 삼는다. 끝나면 멈춘다.

### 출처
- Official: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/03-deployment/homework.md — Question 1
- Starter (fork): https://github.com/alexeygrigorev/agent-relay

### 학습 목표
Agent Relay를 로컬에서 실행·만져 보고, Q1 객관식에 답한다.

### 초보자가 할 일 (순서 고정)
1. https://github.com/alexeygrigorev/agent-relay 를 **Fork** 한다.
2. Fork를 `E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay\` 로 클론한다.  
   - 이미 `_docs/`·`AIDT_03_HW.md`·`AGENTS.md`가 있으면 **덮어쓰지 말고** 스타터 파일만 합친다 (guides 유지).
3. `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1` 후 README대로 **로컬 실행**.
4. 대시보드·API를 열어 “누가 메시지를 어디에 두는가”를 관찰한다.
5. Q1에 답해 `AIDT_03_HW.md`에 적는다.

### Coding agent prompt
```text
Read the Agent Relay README and run the project locally on Windows.
Use E: caches via use_e_drive.ps1. Do not invent cloud deploy.
Summarize in 5 bullets: how to start, where the API listens, where data lives,
what the dashboard shows, how agents interact.
```

### Q1 선택지
Which description matches the project's architecture?
- Agents exchange tasks directly with each other.
- Agents claim tasks from a DB through an HTTP API.
- Agents consume tasks from a message broker.
- The browser stores and executes tasks.

### 완료 기준
- [ ] Fork + 클론 (guides 유지)
- [ ] 앱이 로컬에서 뜸
- [ ] Q1 → `AIDT_03_HW.md`
- [ ] (선택) Gemini 노트 → `_docs/notes/01-understand-project.md`

### 하지 말 것
Dockerfile, Compose, kind, CI — 다음 패킷.
