# 재미나이 지침 — Packet 06 / Q6 (Watch the agent fix the incident)

아래 **「복붙 블록」** 전체를 재미나이 새 채팅에 넣고, 그 아래에 `packets/06-watch-agent-fix.md` 본문을 붙인다.  
한 패킷만. 끝나면 「HW4 공식 문제는 여기까지. 제출은 학습자」로 멈춘다.

---

## 복붙 블록 (래퍼 + 형식 규칙)

```text
역할: AIDT Module 04 Homework 4 — Packet 06 (Q6 Watch the agent fix the incident) 초보자용 한글 내러티브만 작성한다.

범위:
- 아래 붙은 「Packet 06」내용만.
- AWS / Agent Relay 제출 경로 금지.
- 없는 URL·경로·명령을 만들지 말 것.
- 스타터: https://github.com/alexeygrigorev/order-tracker
- 앱 경로: E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker\
- 작업: E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\HW_04\
- 메모장: E:\IT_SPACES\AI\zoomcamp_misc\AIDT\04\AIDT_HW_04.txt
- 제출 답 파일: AIDT_04_HW.md Q6 행
- 이전 사실: Q1 ok / Q2 200 / Q3 404 / Q4 Normal / Q5 last line standing down

문서 형식:
1. 서두에 「Q6 문제」영문 MCQ 원문 + 초보 한 줄.
2. 중간에 실행 가이드 (PowerShell 복붙). 에이전트 프롬프트 → webhook 연결 → curl express-1002 (반복) → Grafana Firing/webhook → headless 수정 → 앱 재시작 → 재검증 → MCQ.
3. 말미에 「Q6 체크리스트」만.
4. 정답(네 선택지 중 하나)을 단정하지 말 것. 재현·수정 후 본 원인으로 고르라고 할 것.
5. 끝나면 「HW4 공식 문제는 여기까지. 제출(commit/push/폼)은 학습자」.

초보가 반드시 이해해야 할 포인트:
- Order Tracker이지 Agent Relay가 아니다.
- Q5는 테스트 알림. Q6은 진짜 Grafana webhook + express-1002.
- 알림이 안 뜨면 curl을 여러 번.
- Grafana(컨테이너) → host responder는 host.docker.internal:8001 등이 필요할 수 있음.
- Cursor CLI 실수정에는 agent login / CURSOR_API_KEY가 필요할 수 있음.
- cwd는 order-tracker. 데이터는 E:만.

출력: 메모장에 붙여넣을 수 있는 한글 마크다운 한 편.
```

---

## 그 아래에 붙일 패킷

파일: `DevOps/HW_04/_docs/guides/packets/06-watch-agent-fix.md` (전체 복사)
