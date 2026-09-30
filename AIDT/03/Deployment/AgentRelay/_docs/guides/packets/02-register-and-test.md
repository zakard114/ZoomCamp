# Packet 02 — Register agents and test the task flow / 등록·태스크 흐름 (Q2)

### 전제
Packet 01 완료. 로컬 Agent Relay 실행 가능. `SPEC.md` 존재.

### 출처
- homework.md Question 2
- starter repo root `SPEC.md` (first acceptance scenario)
- Official HW: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp/blob/main/cohorts/2026/homework/03-deployment/homework.md

### 학습 목표
에이전트 2개를 등록하고 태스크·결과를 교환한 뒤, 같은 흐름을 **API 통합 테스트**로 고정한다.

### 초보자가 할 일
1. `SPEC.md` 첫 acceptance scenario를 읽는다.
2. 에이전트 2 등록 → 태스크 교환 → 대시보드에서 결과 확인 (직접 클릭/요청).
3. 코딩 에이전트에게 이 흐름을 **실제 API+DB** 대상 통합 테스트로 만들게 한다.
4. 테스트를 실행해 통과를 확인한다.
5. Q2 MCQ에 답한다.

### Coding agent prompt
```text
Read SPEC.md. Help me run the first acceptance scenario locally:
register two agents, exchange a task and its result, verify on the dashboard.
Then add an API integration test against the real API and DB for this flow.
Run the test and show it passing. Do not add Kubernetes or Compose yet.
```

### Q2 선택지
Which task status does the sender see after the recipient submits its result?
- `queued`
- `processing`
- `completed`
- `delivered`

### 완료 기준
- [ ] 수동 시나리오 성공
- [ ] 통합 테스트 통과
- [ ] Q2 → `AIDT_03_HW.md`

### 하지 말 것
Dockerfile / Compose / kind / CI.
