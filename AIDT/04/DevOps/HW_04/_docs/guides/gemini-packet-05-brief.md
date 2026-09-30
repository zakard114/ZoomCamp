# 재미나이 지침 — Packet 05 / Q5 (Build the automatic responder)

아래 **「복붙 블록」** 전체를 재미나이 새 채팅에 넣고, 그 아래에 `packets/05-automatic-responder.md` 본문을 붙인다.  
한 패킷만. 끝나면 「다음 패킷은 허락 후」로 멈춘다.

---

## 복붙 블록 (래퍼 + 형식 규칙)

```text
역할: AIDT Module 04 Homework 4 — Packet 05 (Q5 Build the automatic responder) 초보자용 한글 내러티브만 작성한다.

범위:
- 아래 붙은 「Packet 05」내용만.
- Grafana webhook 연결 / express-1002 실사고 / Agent Relay / AWS 금지 (Q6).
- 없는 URL·경로·명령을 만들지 말 것.
- 스타터: https://github.com/alexeygrigorev/order-tracker
- 앱 경로: E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\order-tracker\
- 작업: E:\IT_SPACES\AI\ZoomCamp\AIDT\04\DevOps\HW_04\
- 메모장: E:\IT_SPACES\AI\zoomcamp_misc\AIDT\04\AIDT_HW_04.txt
- 제출 답 파일: AIDT_04_HW.md Q5 행
- 이전 사실: Q1 ok / Q2 metric 200 / Q3 metric 404 / Q4 alert Normal

문서 형식:
1. 서두에 「Q5 문제」영문 원문 + 초보 한 줄. (객관식 아님 — 에이전트 응답 마지막 줄 포함)
2. 중간에 실행 가이드 (PowerShell 복붙). 에이전트 프롬프트 → 리스폰더 :8001 기동 → 테스트 curl → 응답 파일/로그 읽기.
3. 말미에 「Q5 체크리스트」만.
4. 에이전트가 뭐라고 답할지 지어내지 말 것. 저장된 응답을 보고 적으라고 할 것.
5. 끝나면 「다음 패킷(Packet 06)은 허락 후」.

초보가 반드시 이해해야 할 포인트:
- Order Tracker이지 Agent Relay가 아니다.
- Q5는 webhook 연결 전: curl로 POST /alerts 테스트.
- 테스트 페이로드는 ResponderTest / test=true / no incident to fix.
- 답은 free-text. 마지막 줄을 꼭 포함.
- cwd는 order-tracker. 데이터는 E:만.

출력: 메모장에 붙여넣을 수 있는 한글 마크다운 한 편.
```

---

## 그 아래에 붙일 패킷

파일: `DevOps/HW_04/_docs/guides/packets/05-automatic-responder.md` (전체 복사)
