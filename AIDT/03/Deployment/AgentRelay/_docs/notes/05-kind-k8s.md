# AIDT 03 — Packet 05 / Question 5
# Deploy to Kubernetes (kind)

## 문제 (What is Q5?)

kind 클러스터에 Agent Relay + PostgreSQL을 올리고,
어떤 리소스가 **원하는 replica 수를 유지하고 업데이트를 관리**하는지 고른다.

Which Kubernetes resource keeps the requested number of application replicas running and manages updates?

- Service
- ConfigMap
- Deployment
- Secret

제출: `AIDT_03_HW.md` Q5 행

---

## 당신이 실행할 것 (Cursor가 대신 돌리지 않음)

0. Docker Desktop ON. Compose가 8000을 쓰면 port-forward와 충돌하니 잠시 내림:
   `docker compose down`

1. kind PATH (세션마다):
```powershell
cd E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay
. E:\IT_SPACES\AI\scripts\use_e_drive.ps1
$env:Path = "E:\IT_SPACES\AI\.cache\bin;$env:Path"
kind version
kubectl version --client
```

2. 클러스터 생성 (E: pgdata 마운트 포함):
```powershell
kind create cluster --config k8s/kind-config.yaml
```

3. 이미지 빌드 → kind에 로드:
```powershell
docker build -t agent-relay:local .
kind load docker-image agent-relay:local --name agent-relay
```

4. 매니페스트 적용 (postgres 먼저):
```powershell
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/api.yaml
kubectl get pods -w
# Ready 되면 Ctrl+C
```

5. 포트포워드 (새 터미널도 가능):
```powershell
kubectl port-forward svc/agent-relay 8000:8000
```

6. 확인:
   - http://127.0.0.1:8000/health
   - Q2 흐름 (등록 → 태스크 → claim → complete)
   - 대시보드 http://127.0.0.1:8000/

정리 (선택):
```powershell
kind delete cluster --name agent-relay
```

---

## 정답 (Q5 Answer)

**`Deployment`** — `replicas`를 유지하고 RollingUpdate 등 배포를 관리한다.

| 선택지 | 판정 |
|--------|------|
| Service | ❌ Pod에 안정적인 네트워크 이름/포트 |
| ConfigMap | ❌ 설정 데이터 |
| **Deployment** | ✅ replica + 업데이트 |
| Secret | ❌ 민값/키 |

---

## Checklist (당신이 확인 후 체크)

- [ ] kind 클러스터 + `k8s/` 적용
- [ ] Pod Ready + port-forward + 태스크 흐름
- [ ] Q5 → `AIDT_03_HW.md`
- [ ] 이 노트·브리프 확인
