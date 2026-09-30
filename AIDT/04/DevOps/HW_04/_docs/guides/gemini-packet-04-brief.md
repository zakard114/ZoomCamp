# 재미나이 지침 — Packet 04 / Q4 (Configure the alert)

아래 **「복붙 블록」** 전체를 재미나이 새 채팅에 넣고, 그 아래에 `packets/04-configure-alert.md` 본문을 붙인다.  
한 패킷만. 끝나면 「다음 패킷은 허락 후」로 멈춘다.

---

## 복붙 블록 (래퍼 + 형식 규칙)

```text
역할: AIDT Module 04 Homework 4 — Packet 04 (Q4 Configure the alert) 초보자용 한글 내러티브만 작성한다.

범위:
- 아래 붙은 「Packet 04」내용만.
- incident-response / webhook 연결 / headless agent / Agent Relay / AWS 금지 (Q5–Q6).
- 없는 URL·경로·명령을 만들지 말 것.
- 스타터: https://github.com/alexeygrigorev/order-tracker
- 앱 경로: E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker\
- 작업: E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\HW_04\
- 메모장: E:\IT_SPACES\AI\zoomcamp_misc\AIDT\04\AIDT_HW_04.txt
- 제출 답 파일: AIDT_04_HW.md Q4 행
- 이전 사실 한 줄씩: Q1 healthz → {"status":"ok"} / Q2 standard-1001 metric → 200 / Q3 standard-1002 metric → 404

문서 형식:
1. 서두에 「Q4 문제」영문 MCQ 원문 + 초보 한 줄.
2. 중간에 실행 가이드 (PowerShell 복붙). 에이전트 프롬프트 → compose → curl standard-1002 → Grafana alert state 확인.
3. 말미에 「Q4 체크리스트」만.
4. 정답(Normal/Firing/Pending/No data)을 단정하지 말 것. Grafana alert UI state를 보고 고르라고 할 것.
5. 끝나면 「다음 패킷(Packet 05)은 허락 후」.

초보가 반드시 이해해야 할 포인트:
- 이 숙제 앱은 Order Tracker이지 Agent Relay가 아니다.
- alert는 5xx를 본다. Q3의 standard-1002는 404였고, 404 ≠ 5xx.
- webhook·responder는 아직(Q6). 지금은 Grafana에서 state만 확인.
- 프롬프트 cwd는 order-tracker 폴더.
- 포트 충돌 시 ORDER_TRACKER_PORT / compose에 적힌 Grafana 포트 사용.

출력: 메모장에 붙여넣을 수 있는 한글 마크다운 한 편.
```

---

## 그 아래에 붙일 패킷

파일: `DevOps/HW_04/_docs/guides/packets/04-configure-alert.md` (전체 복사)
