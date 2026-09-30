# AIDT 03 — Packet 04 / Question 4
# Docker Compose and PostgreSQL

## 문제 (What is Q4?)

SQLite를 PostgreSQL로 바꾸고, `compose.yaml`로 앱 + DB를 함께 띄운다.
DB 서비스 이름은 **`postgres`**.

Which hostname should the API use to connect to the `postgres` service in Docker Compose?

- `localhost`
- `postgres`
- `host.docker.internal`
- `0.0.0.0`

제출: `AIDT_03_HW.md` Q4 행

---

## 당신이 실행할 것 (Cursor가 대신 돌리지 않음)

0. Docker Desktop ON. 기존 `agent-relay-local` 컨테이너가 8000을 쓰면 중지:
   `docker rm -f agent-relay-local`

1. 작업 폴더:
   `cd E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay`
   `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1`

2. 스택 기동:
   `docker compose up --build`

3. 다른 터미널 — health:
   `Invoke-RestMethod http://127.0.0.1:8000/health`

4. Q2 통합 테스트 (호스트 → Compose의 공개 Postgres 5432):
```powershell
$env:RELAY_DATABASE_URL = "postgresql+psycopg://relay:relay@127.0.0.1:5432/relay"
# 주의: pytest는 시작 시 DB 테이블을 drop/create 함. API 컨테이너와 같은 DB를 쓰면 데이터가 지워짐.
# 숙제 의도대로라면 테스트용 DB를 쓰거나, 스택을 잠시 내리고 테스트 후 다시 up.
```
간단 확인: 대시보드에서 태스크 한 사이클 후
`docker compose exec postgres psql -U relay -d relay -c "SELECT id, status FROM tasks ORDER BY created_at DESC LIMIT 5;"`

---

## 정답 (Q4 Answer)

**`postgres`** — Compose 네트워크 안에서는 서비스 이름이 DNS 호스트명.

| 선택지 | 판정 |
|--------|------|
| `localhost` | ❌ 컨테이너 자기 자신 |
| **`postgres`** | ✅ compose 서비스명 |
| `host.docker.internal` | ❌ 호스트 OS 접근용 |
| `0.0.0.0` | ❌ bind 주소 |

---

## Checklist (당신이 확인 후 체크)

- [ ] `compose.yaml` + `docker compose up --build`
- [ ] 통합 테스트 또는 대시보드+psql로 Postgres 저장 확인
- [ ] Q4 → `AIDT_03_HW.md`
- [ ] 이 노트 저장
