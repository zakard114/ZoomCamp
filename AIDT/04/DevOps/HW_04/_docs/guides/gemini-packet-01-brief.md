# 재미나이 지침 — Packet 01 / Q1 (Run the app)

아래 **「복붙 블록」** 전체를 재미나이 새 채팅에 넣고, 그 아래에 `packets/01-run-the-app.md` 본문을 붙인다.  
한 패킷만. 끝나면 「다음 패킷은 허락 후」로 멈춘다.

---

## 복붙 블록 (래퍼 + 형식 규칙)

```text
역할: AIDT Module 04 Homework 4 — Packet 01 (Q1 Run the app) 초보자용 한글 내러티브만 작성한다.

범위:
- 아래 붙은 「Packet 01」내용만.
- OpenTelemetry / Grafana / 알림 / responder / Agent Relay / AWS 금지.
- 없는 URL·경로·명령을 만들지 말 것.
- 스타터: https://github.com/alexeygrigorev/order-tracker
- 클론 경로: E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker\
- 메모장: E:\IT_SPACES\AI\zoomcamp_misc\AIDT\04\AIDT_HW_04.txt
- 제출 답 파일: AIDT_04_HW.md Q1 행

문서 형식:
1. 서두에 「Q1 문제」영문 MCQ 원문 + 초보 한 줄.
2. 중간에 실행 가이드 (PowerShell 복붙). Fork → clone → Docker 엔진 확인 → compose up → 브라우저 → curl healthz.
3. 말미에 「Q1 체크리스트」만.
4. 정답을 단정하지 말 것. curl에 찍힌 JSON을 보고 고르라고 할 것.
5. 끝나면 「다음 패킷(Packet 02)은 허락 후」.

초보가 반드시 이해해야 할 포인트:
- 이 숙제 앱은 Order Tracker이지 Agent Relay가 아니다.
- health 경로가 /healthz 이다 (/health 아님).
- 프롬프트는 E:\IT_SPACES\AI 가 아니라 order-tracker 폴더여야 한다.
- Docker Engine stopped면 compose는 실패한다.

출력: 메모장에 붙여넣을 수 있는 한글 마크다운 한 편.
```

---

## 그 아래에 붙일 패킷

파일: `DevOps/HW_04/_docs/guides/packets/01-run-the-app.md` (전체 복사)
