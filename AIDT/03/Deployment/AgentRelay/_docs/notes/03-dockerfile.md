# AIDT 03 — Packet 03 / Question 3
# Containerization / 컨테이너화

---

## 문제 (What is Q3?)

Agent Relay용 `Dockerfile`을 만들고 이미지를 `agent-relay:local`로 빌드한 뒤,  
API 포트를 **내 머신에 공개**한 채 컨테이너로 실행한다.  
(컨테이너 안 uvicorn은 `--host 0.0.0.0` — 기본 `127.0.0.1`이면 `-p`가 안 되는 것처럼 보임.)

Which Docker option publishes a container's port to your machine?

- `--expose`
- `-p`
- `-v`
- `--name`

제출: `AIDT_03_HW.md` Q3 행

---

## 한 일

1. `Dockerfile` + `.dockerignore` 추가
2. `docker build -t agent-relay:local .`
3. `docker run ... -p 8000:8000 agent-relay:local`  (호스트 포트 공개 = **`-p`**)
4. 컨테이너 API로 Q2 태스크 흐름 재확인

---

## 정답 (Q3 Answer)

**`-p`**

| 옵션 | 판정 | 뜻 |
|------|------|-----|
| `--expose` | ❌ | 이미지 메타데이터에 포트 문서화 (호스트에 안 염) |
| **`-p`** | ✅ | 호스트:컨테이너 포트 매핑 (publish) |
| `-v` | ❌ | 볼륨 마운트 |
| `--name` | ❌ | 컨테이너 이름 |

---

## Checklist

- [x] `agent-relay:local` 빌드·실행 (`0.0.0.0` bind)
- [x] 컨테이너 상대로 태스크 흐름 확인 (`SENDER_STATUS completed`)
- [x] Q3 → `AIDT_03_HW.md`
- [x] 노트 `03-dockerfile.md` 저장
