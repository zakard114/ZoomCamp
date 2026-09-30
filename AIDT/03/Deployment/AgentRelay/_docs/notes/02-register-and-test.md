# AIDT 03 — Packet 02 / Question 2
# Register agents and test the task flow / 등록·태스크 흐름

---

## 문제 (What is Q2?)

에이전트 2명을 등록하고 태스크를 주고받은 뒤,  
**수신자가 결과를 제출한 다음, 송신자(sender)가 보는 task status**가 무엇인지 고른다.

Which task status does the sender see after the recipient submits its result?

- [ ] `queued`
- [ ] `processing`
- [ ] `completed`
- [ ] `delivered`

제출 기록 위치: `AIDT_03_HW.md` 표 **Q2** 행  
학습 노트 위치: 이 파일 (`_docs/notes/02-register-and-test.md`)  
따라하기 상세: [`01b-dashboard-walkthrough.md`](01b-dashboard-walkthrough.md)

---

## 초보 네러티브 (왜 이 문제인가)

Q1에서 “HTTP + DB + claim” 구조를 알았다.  
Q2는 그 구조로 **실제로 한 사이클**을 돌리고, 끝난 뒤 sender 조회 결과가 뭔지 확인한다.

상태 흐름 (이 프로토콜):

```text
queued → processing → completed
```

`delivered` 라는 status는 **없다**.

---

## 실습 요약 (우리가 한 일)

1. alice / bob 등록 (`POST /api/v1/agents`) → token 메모  
2. 대시보드: alice token → **Use token**  
3. alice → bob 태스크 (`POST /tasks`) → Status **`queued`**  
4. bob **claim** → (60초 lease 안에) Status **`processing`**  
5. bob **complete** → alice `GET /tasks/{id}` → Status **`completed`**  
6. 대시보드 Refresh → `completed`, Output `HELLO PACKET02`

**주의 (실습에서 배운 것):** lease 기본 60초. claim만 하고 오래 보면 `expired` 후 다시 `queued`.  
`processing`을 보려면 claim 직후 바로 Refresh. complete는 lease 만료 전에.

통합 테스트: `test_sender_sees_completed_after_recipient_result` 포함 **5 passed**.

---

## 실습 증거 (핵심만)

- task_id: `task_b5028016529444d4a418d8694b832fa4`
- 터미널 complete 후: `status = completed`
- 대시보드 최종:

| Status | Output | Delivery history (끝) |
|--------|--------|------------------------|
| completed | HELLO PACKET02 | 5:completed (manual-ps1) |

(1~4 expired = lease 타임아웃 흔적. 정상.)

---

## 정답 (Q2 Answer)

**`completed`**

| 선택지 | 판정 | 이유 |
|--------|------|------|
| `queued` | ❌ | 보낸 직후·미claim |
| `processing` | ❌ | claim 직후·미complete |
| **`completed`** | ✅ | recipient가 complete한 뒤 sender GET |
| `delivered` | ❌ | 이 프로토콜 lifecycle에 없음 |

`AIDT_03_HW.md` Q2 행에 기록 완료.

---

## Packet 02 Checklist

- [x] 수동 시나리오 성공 (등록 → 태스크 → claim → complete → sender 확인)
- [x] 통합 테스트 통과 (5 passed)
- [x] Q2 정답을 `AIDT_03_HW.md`에 작성 완료
- [x] 이 노트 저장 완료

**Packet 02 끝.** 다음(Packet 03 Dockerfile)은 허락 후.
