# AIDT 03 — Packet 06 / Question 6
# CI/CD with act

## 문제 (What is Q6?)

테스트가 실패하면 이 워크플로에서 무엇이 일어나야 하나?

What should happen if a test fails in this workflow?

- Deploy the new version and report the failure.
- Keep the existing version running and stop the deployment.
- Delete the existing deployment.
- Deploy the previous image with the new tag.

제출: `AIDT_03_HW.md` Q6 행

---

## 당신이 실행할 것

0. Docker Desktop ON. kind 클러스터 `agent-relay` 살아 있어야 함 (Packet 05).
   PATH:
```powershell
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
$env:Path = "E:\IT_SPACES\AI\.cache\bin;C:\Program Files\Docker\Docker\resources\bin;$env:Path"
```

1. **첫 CI 실행** (테스트 → 통과 시에만 kind 배포):
```powershell
.\scripts\run-act-ci.ps1
```
- `act -j test` 가 실패하면 **배포를 하지 않음** → 기존 Deployment 유지 (Q6).
- 성공 시 고유 태그로 이미지 빌드 → `kind load` → `kubectl set image` → rollout 대기.

2. port-forward 후 health 확인:
```powershell
kubectl port-forward svc/agent-relay 8000:8000
# 다른 창: Invoke-RestMethod http://127.0.0.1:8000/health
```

3. **v2 롤아웃:** `dashboard.html` 의 `<h1>Agent Relay</h1>` → `<h1>Agent Relay v2</h1>`
   (title도 같이 바꿔도 됨). 저장 후 다시:
```powershell
.\scripts\run-act-ci.ps1
```
   브라우저에서 제목 `Agent Relay v2` 확인 (캐시면 Ctrl+F5).

워크플로 원본: `.github/workflows/ci.yml`  
로컬 엔트리: `scripts/run-act-ci.ps1` (Windows에서 act 컨테이너 → host kind 연결이 까다로워, 테스트는 act / 배포는 호스트 kubectl·kind).

---

## 정답 (Q6 Answer)

**Keep the existing version running and stop the deployment.**

| 선택지 | 판정 |
|--------|------|
| Deploy the new version and report the failure | ❌ 깨진 버전을 올리면 안 됨 |
| **Keep the existing version running and stop the deployment** | ✅ `needs: test` — 테스트 실패 시 deploy job 미실행 |
| Delete the existing deployment | ❌ 운영 중인 걸 지울 이유 없음 |
| Deploy the previous image with the new tag | ❌ 새 태그로 옛 이미지를 올리는 게 아님 |

---

## Checklist

- [ ] `.\scripts\run-act-ci.ps1` 성공 (테스트 + 배포)
- [ ] dashboard `Agent Relay v2` 후 재실행·롤아웃 확인
- [ ] Q6 → `AIDT_03_HW.md` (+ reflection 한 줄)
- [ ] 이 노트·브리프 확인
