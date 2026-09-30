# 재미나이 지침 — Packet 03 / Q3 (Build the telemetry pipeline)

아래 **「복붙 블록」** 전체를 재미나이 새 채팅에 넣고, 그 아래에 `packets/03-telemetry-pipeline.md` 본문을 붙인다.  
한 패킷만. 끝나면 「다음 패킷은 허락 후」로 멈춘다.

---

## 복붙 블록 (래퍼 + 형식 규칙)

```text
역할: AIDT Module 04 Homework 4 — Packet 03 (Q3 Build the telemetry pipeline) 초보자용 한글 내러티브만 작성한다.

범위:
- 아래 붙은 「Packet 03」내용만.
- Grafana 5xx 알림 / incident-response / webhook / headless agent / Agent Relay / AWS 금지 (Q4+).
- 없는 URL·경로·명령을 만들지 말 것.
- 스타터: https://github.com/alexeygrigorev/order-tracker
- 앱 경로: E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker\
- 작업: E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\HW_04\
- 메모장: E:\IT_SPACES\AI\zoomcamp_misc\AIDT\04\AIDT_HW_04.txt
- 제출 답 파일: AIDT_04_HW.md Q3 행
- Packet 01·02 사실만 한 줄씩: healthz → {"status":"ok"} / standard-1001 metric → 200 (console)

문서 형식:
1. 서두에 「Q3 문제」영문 MCQ 원문 + 초보 한 줄.
2. 중간에 실행 가이드 (PowerShell 복붙). 에이전트 프롬프트 → compose rebuild → curl -i standard-1002 → Grafana에서 request metric (+ log/trace 확인).
3. 말미에 「Q3 체크리스트」만.
4. 정답(404/200/301/500)을 단정하지 말 것. Grafana의 request metric에 찍힌 status를 보고 고르라고 할 것.
5. 끝나면 「다음 패킷(Packet 04)은 허락 후」.

초보가 반드시 이해해야 할 포인트:
- 이 숙제 앱은 Order Tracker이지 Agent Relay가 아니다.
- Q2는 콘솔 export. Q3는 Collector + Prometheus + Loki + Tempo + Grafana.
- 최종 답은 curl이 아니라 Grafana request metric의 HTTP status.
- 데이터/볼륨은 E: 만. C:\Users 금지.
- 프롬프트 cwd는 order-tracker 폴더.
- 포트 충돌 시 compose에 적힌 포트로 Grafana에 접속.

출력: 메모장에 붙여넣을 수 있는 한글 마크다운 한 편.
```

---

## 그 아래에 붙일 패킷

파일: `DevOps/HW_04/_docs/guides/packets/03-telemetry-pipeline.md` (전체 복사)
