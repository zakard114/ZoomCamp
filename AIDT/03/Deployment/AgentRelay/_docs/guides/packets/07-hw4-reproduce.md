# Packet 07 — HW4 재현 (백업 코드 사용)

백업은 이미 이 레포에 있다. 이 패킷은 **그 코드를 다시 돌려 보는 지침**이다.  
숙제 공식 릴리즈 전이다. **`git push` 금지.**

### 전제
- 작업 루트: `E:\IT_SPACES\AI\ZoomCamp\AIDT\03\Deployment\AgentRelay`
- 브랜치: `hw4-observability-backup` (로컬만)
- AWS Create stack: 하지 말 것
- 캐시: `. E:\IT_SPACES\AI\scripts\use_e_drive.ps1` 이 멈추면 건너뛰고 `.venv\Scripts\python.exe` 를 직접 쓴다

### 백업 vs 재현
| | 역할 |
|---|---|
| 백업 | 계측, Compose 정의, 알림, 런북, 보고서, `INC-20260925-001` |
| 재현 | 아래 순서로 같은 루프를 **다시** 확인한다. 결과가 같으면 8번 답을 유지한다 |

### 초보자가 할 일 (순서 고정)

1. Docker Desktop ON. 이미 `interview-canvas-obs-*` 가 4318/9090/3000 을 쓰고 있으면 **새로 Compose 올리지 않는다.** 그 Collector를 그대로 쓴다.
2. 포트가 비어 있을 때만:
   `docker compose -f observability/compose.yaml -p agent-relay-obs up -d`
3. 재현 테스트 (토큰은 출력·파일에 남기지 말 것):

```powershell
$env:RELAY_DATABASE_URL = "sqlite:///E:/IT_SPACES/AI/.cache/tmp/agent-relay-hw4-test.db"
$env:OTEL_ENABLED = "0"
$env:OTEL_SDK_DISABLED = "1"
New-Item -ItemType Directory -Force -Path E:\IT_SPACES\AI\.cache\tmp | Out-Null
.\.venv\Scripts\python.exe -m pytest .\test_hw4_inject.py -q --tb=short
```

기대: `1 passed`. 의미: 등록 201 → 플래그 켜면 500 → 끄면 201.

4. (선택) Prometheus가 떠 있으면 브라우저에서 `http://127.0.0.1:9090` 에 `up` 을 넣는다. 캔버스 대시보드가 보여도 괜찮다. 숙제 알림 정의는 `observability/alerts.yaml` 이다.
5. 증거·제안·허가 파일을 읽기만 한다:
   - `incident-response/evidence/INC-20260925-001.json`
   - `incident-response/last-response.json`
   - `incident-response/autonomy-policy.yaml`
   - `docs/operations-and-security-report.md`
6. 폼 답을 `AIDT_04_HW.md` 와 대조한다. 푸시하지 않는다.

### 막히면
- pytest가 `/tmp` sqlite 오류: 3번의 `RELAY_DATABASE_URL` 을 그대로 쓴다.
- 8000이 안 뜬다: live uvicorn은 건너뛴다. 재현의 합격선은 **pytest 1 passed** 다.
- Semgrep이 없다: `security-audit/findings.json` 을 읽고 넘어간다. 릴리즈 후 CLI를 설치해도 된다.

### 완료 기준
- [ ] `test_hw4_inject.py` 1 passed
- [ ] 보고서 5칸을 소리 내어 설명할 수 있다
- [ ] `git push` 를 하지 않았다

### 폼 답 (백업 재현과 같으면 유지)

1. Metrics, logs, and traces
2. OpenTelemetry
3. Grafana
4. Real user impact, with context to start investigating
5. With read-only, allowlisted queries
6. The autonomy policy and allowlists — code outside the model
7. Semgrep
8. INC-20260925-001: POST /api/v1/agents returned 500 so new agents could not enroll. The responder blamed the local inject flag and proposed disable-inject.ps1. Policy allowed that runbook; after the flag was removed, registration returned 201.

저장소 링크는 **푸시 후에만** 폼에 넣는다. 지금은 적어두기만: `https://github.com/zakard114/agent-relay`  
보고서 경로: `docs/operations-and-security-report.md`
