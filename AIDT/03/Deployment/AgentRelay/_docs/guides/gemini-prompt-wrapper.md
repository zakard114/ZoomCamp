# Gemini handoff wrapper (paste above each packet)

재미나이에게 **아래 래퍼 + 해당 패킷 전체**를 그대로 넘긴다. 한 패킷만. 끝나면 멈춰서 허락을 받는다.

Packet 03 전용 강화 지침: [`gemini-packet-03-brief.md`](gemini-packet-03-brief.md)

```text
역할: AIDT Module 03 Homework 3 (Agent Relay + kind) 초보자용 한글 내러티브 가이드를 쓴다.

규칙:
- 아래에 붙은 「소단계 패킷」내용만 사용한다. 없는 URL·명령·경로를 만들지 말 것.
- 스타터는 공식 fork만: https://github.com/alexeygrigorev/agent-relay
- 제목은 English / 한글 병기.
- 서두: 해당 Q 문제(MCQ 원문)를 먼저 명시.
- 말미: 완료 체크리스트만 (✅/❌). 객관식·체크리스트 중복 금지.
- PowerShell 복붙 가능한 명령 블록을 쓸 것. 추상 지시만 금지.
- #### 장식 구분선 금지. Q1/Q2/Q3 구획을 섞지 말 것.
- 코딩 에이전트 프롬프트는 패킷에 있는 것만 (영어 유지 OK).
- AWS·유료 클라우드 금지 (kind 로컬만). Compose/kind는 해당 패킷에서만.
- 끝나면 「다음 패킷은 허락 후」로 멈추기.

출력: 메모장(AIDT_HW_03.txt) / _docs/notes/ 에 붙일 마크다운 한 편.
```

그 아래에 패킷 본문을 붙인다.
