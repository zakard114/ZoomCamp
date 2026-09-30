# 재미나이 지침 — Packet 03 / Q3 (Containerization)

아래 **「복붙 블록」** 전체를 재미나이 새 채팅에 넣고, 그 아래에 `packets/03-dockerfile.md` 본문을 붙인다.  
한 패킷만. 끝나면 「다음 패킷은 허락 후」로 멈춘다.

---

## 복붙 블록 (래퍼 + 형식 규칙)

```text
역할: AIDT Module 03 Homework 3 — Packet 03 (Q3 Containerization) 초보자용 한글 내러티브만 작성한다.

범위:
- 아래 붙은 「Packet 03」내용 + 이미 끝난 Q1/Q2 사실만 사용.
- Compose / Postgres / kind / CI / AWS 금지.
- 없는 URL·경로·명령을 만들지 말 것.
- 스타터 fork: https://github.com/alexeygrigorev/agent-relay
- 작업 경로: E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay\
- 메모장 저장 위치(참고): E:\IT_SPACES\AI\zoomcamp_misc\AIDT\03\AIDT_HW_03.txt
- 제출 답: AIDT_03_HW.md Q3 행 / 노트: _docs/notes/03-dockerfile.md

문서 형식 (필수 — 이전에 Q1/Q2에서 깨진 것 반복 금지):
1. 서두에 「Q3 문제」를 먼저 명시 (영문 MCQ 원문 + 초보 한 줄 설명).
2. 중간에 실행 가이드 (PowerShell 복붙 가능한 명령 블록).
3. 말미에 「Q3 체크리스트」만 (✅/❌). 객관식과 체크리스트를 두 번 쓰지 말 것.
4. Q1·Q2 내용을 이 문서에 길게 재탕하지 말 것. 필요하면 한 줄 링크만.
5. #### 구분선 / 장식용 박스문자 금지.
6. 「Agents, My tasks 버튼」처럼 틀린 UI 말하지 말 것. 대시보드는 관찰창; 포트 공개는 docker -p.
7. 추상 문장 금지. 예: 「Docker로 실행한다」만 쓰지 말고 `docker build` / `docker run -p ...` 를 적을 것.
8. 끝나면 「다음 패킷(Packet 04)은 허락 후」로 멈추기.

초보가 반드시 이해해야 할 포인트:
- 컨테이너 안 uvicorn은 --host 0.0.0.0 (127.0.0.1이면 -p가 깨진 것처럼 보임).
- 이미지 이름 고정: agent-relay:local
- MCQ 정답 후보 설명: --expose / -p / -v / --name 차이를 초보 말로 (정답은 -p).

출력: 메모장에 붙여넣을 수 있는 한글 마크다운 한 편.
제목 예: Packet 03 — Containerization / 컨테이너화 (Q3)
```

---

## 그 아래에 붙일 패킷

파일: `Deployment/AgentRelay/_docs/guides/packets/03-dockerfile.md`  
(전체 복사)

---

## 재미나이 출력 받은 뒤 (학습자/Cursor)

1. 타당성: Dockerfile에 `0.0.0.0` 있는지, 명령이 PowerShell인지, Compose가 끼지 않았는지.
2. 통과하면 `AIDT_HW_03.txt` 의 Packet 03 구획에 반영 (서두=문제, 말미=체크리스트).
3. `_docs/notes/03-dockerfile.md` · `AIDT_03_HW.md` Q3 와 모순 없는지 맞춤.
