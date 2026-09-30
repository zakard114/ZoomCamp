# Packet 05 — Deploy to Kubernetes (kind) / kind 배포 (Q5)

### 전제
Packet 04 완료.

### 출처
- homework.md Question 5
- https://kind.sigs.k8s.io/

### 학습 목표
kind 클러스터 + `k8s/` 매니페스트(Agent Relay, PostgreSQL, Service, 스토리지, readiness). 이미지 로드 후 배포, 포트포워드로 Q2 흐름 검증.

### 초보자가 할 일
1. kind·kubectl 설치 여부 확인 (없으면 에이전트에게 E: 경로로 설치).
2. 클러스터 생성.
3. `k8s/` 매니페스트 작성·적용, 이미지 kind에 로드.
4. Pod Ready 확인 → port-forward → 대시보드에서 태스크 흐름.
5. Q5 MCQ에 답한다.

### Coding agent prompt
```text
Install kind and kubectl on Windows if needed (install under E:\IT_SPACES\AI, not C:\Users).
Create a kind cluster. Add k8s/ manifests for Agent Relay and PostgreSQL including
Services, persistent DB storage, and readiness checks.
Load agent-relay:local (or the current image) into kind and deploy.
Show commands to wait for Ready pods and port-forward the dashboard.
Verify the Q2 task flow. No GitHub Actions/act yet.
```

### Q5 선택지
Which Kubernetes resource keeps the requested number of application replicas running and manages updates?
- Service
- ConfigMap
- Deployment
- Secret

### 완료 기준
- [ ] kind 클러스터 + `k8s/` 적용
- [ ] Pod Ready + 태스크 흐름 확인
- [ ] Q5 → `AIDT_03_HW.md`

### 하지 말 것
act / CI 워크플로 (다음 패킷).
