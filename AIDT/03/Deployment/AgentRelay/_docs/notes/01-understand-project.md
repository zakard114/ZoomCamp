# AIDT 03 — Packet 01 / Question 1
# Understand the project / 프로젝트 이해하기

---

## 문제 (What is Q1?)

Agent Relay를 로컬에서 실행·관찰한 뒤, **아키텍처**가 아래 중 무엇인지 고른다.

Which description matches the project's architecture?

- [ ] Agents exchange tasks directly with each other.
- [ ] Agents claim tasks from a DB through an HTTP API.
- [ ] Agents consume tasks from a message broker.
- [ ] The browser stores and executes tasks.

제출 기록 위치: `AIDT_03_HW.md` 표 **Q1** 행  
학습 노트 위치: 이 파일 (`_docs/notes/01-understand-project.md`)

---

## 초보 네러티브 (왜 이 문제인가)

Agent Relay는 에이전트끼리 **일(Task)을 주고받는 작은 메신저**다.  
배포·Docker·kind는 나중이고, **Q1은 “내부 구조가 뭐냐”만** 맞히면 된다.

네 가지 후보를 초보 말로:

| 선택지 | 뜻 |
|--------|-----|
| 서로 직접 통신 | A가 B 주소로 바로 보냄 (P2P) |
| HTTP API로 DB에서 claim | 중앙 서버+DB에 쌓고, HTTP로 “내 일 가져가기” |
| 메시지 브로커 | Kafka/Rabbit 구독 |
| 브라우저가 저장·실행 | 웹이 일 저장하고 실행 |

---

## 한 일 (Q1 범위만)

1. Fork: https://github.com/zakard114/agent-relay (upstream: alexeygrigorev/agent-relay)
2. Clone/병합: `E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay\` (`_docs/` 유지)
3. 로컬 실행: `use_e_drive.ps1` → uvicorn → http://127.0.0.1:8000/
4. 관찰: 대시보드는 **관찰창**일 뿐. 등록/claim은 API. 데이터는 **SQLite** (`agent-relay.db`).

(긴 alice/bob claim·complete 실습 로그는 **Q2 노트**에 둠. 링크: [`02-register-and-test.md`](02-register-and-test.md), [`01b-dashboard-walkthrough.md`](01b-dashboard-walkthrough.md))

---

## Coding-agent 5 bullets

1. **Start:** E: 캐시 후 `uvicorn main:app --host 127.0.0.1 --port 8000`
2. **API:** `http://127.0.0.1:8000` (`/health`, `/ready`, `/api/v1/...`)
3. **Data:** SQLite `./agent-relay.db` (`database.py` / `storage.py`)
4. **Dashboard:** 토큰으로 목록·태스크 **보기만**
5. **Agents:** HTTP + Bearer로 create / claim / complete (브로커·P2P 없음)

---

## 정답 (Q1 Answer)

**Agents claim tasks from a DB through an HTTP API.**

| 선택지 | 판정 | 이유 |
|--------|------|------|
| Agents exchange tasks directly with each other | ❌ | 서로 직접 안 보냄. Relay(API+DB) 경유 |
| **Agents claim tasks from a DB through an HTTP API** | ✅ | SQLite에 저장, `POST /tasks/claim` 등 HTTP로 claim |
| Agents consume tasks from a message broker | ❌ | Kafka/Rabbit 없음 |
| The browser stores and executes tasks | ❌ | 브라우저는 대시보드만 |

`AIDT_03_HW.md` Q1 행에 기록 완료.

---

## Packet 01 Checklist

- [x] Fork 및 지정 경로 클론 완료 (기존 가이드 파일 유지)
- [x] 앱이 로컬 환경에서 정상 구동됨 (`/health` ok)
- [x] Q1 정답을 `AIDT_03_HW.md`에 작성 완료
- [x] 이 노트를 `_docs/notes/01-understand-project.md`에 저장 완료

**Packet 01 끝.** 다음(Packet 02)은 허락 후.
