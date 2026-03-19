# TaskManager 및 Flink 실행 가이드 (한글 번역)

## TaskManager는 실제 작업 수행자입니다

TaskManager는 워커(worker)입니다. 실제 데이터 처리를 실행합니다:

```yaml
taskmanager:
  image: pyflink-workshop                    # jobmanager 서비스가 빌드한 이미지를 그대로 재사용합니다. 별도 빌드 불필요.
  pull_policy: never                         # 로컬에서 빌드한 이미지만 사용하므로, Docker Hub에서 가져오지 않습니다.
  expose:
    - "6121"                                 # TaskManager 간 통신용 데이터 포트 1
    - "6122"                                 # TaskManager 간 통신용 데이터 포트 2
  volumes:
    - ./:/opt/flink/usrlib                   # 로컬 프로젝트 루트를 Flink 라이브러리 경로에 마운트합니다.
    - ./src/:/opt/src                        # 소스 코드(src/)를 컨테이너의 /opt/src에 마운트합니다.
  depends_on:
    - jobmanager                             # jobmanager가 먼저 기동된 뒤에 TaskManager를 시작합니다.
  command: taskmanager --taskmanager.registration.timeout 5 min  # TaskManager로 실행하며, JobManager 연결 대기 시간을 5분으로 설정합니다.
  environment:
    - |
      FLINK_PROPERTIES=
      jobmanager.rpc.address: jobmanager           # JobManager(조정자)의 주소를 지정합니다.
      taskmanager.memory.process.size: 1728m       # 이 TaskManager가 사용할 프로세스 메모리 크기입니다.
      taskmanager.numberOfTaskSlots: 15            # 이 TaskManager가 가진 task 슬롯 개수입니다. (15개)
      parallelism.default: 3                        # 기본적으로 각 파이프라인 단계를 3개의 병렬 복제본으로 실행합니다.
```

### 설정 항목 설명

| 항목 | 설명 |
|------|------|
| `image: pyflink-workshop` | jobmanager 서비스가 빌드한 이미지를 재사용합니다. 별도 `build` 설정 없음. |
| `depends_on: jobmanager` | jobmanager가 먼저 올라온 후에 TaskManager를 시작합니다. |
| `--taskmanager.registration.timeout 5 min` | 서비스가 함께 기동될 때, TaskManager가 JobManager를 최대 5분까지 기다립니다. |
| `taskmanager.numberOfTaskSlots: 15` | 이 TaskManager는 15개의 슬롯을 가집니다. |
| `parallelism.default: 3` | 기본적으로 각 파이프라인 단계가 3개의 병렬 복제본으로 실행됩니다. |

### Task Slot이란?

**Task slot**은 하나의 파이프라인 단계를 병렬로 실행할 수 있는 리소스 단위(메모리, CPU)입니다.  
고속도로의 차선처럼 슬롯이 많을수록 더 많은 데이터를 동시에 처리할 수 있습니다.

- 병렬도(parallelism)가 3인 job을 제출하면 → 3개의 슬롯을 사용합니다.
- 15개의 슬롯이 있으면 → 이 하나의 TaskManager에서 최대 5개의 그런 job을 동시에 실행할 수 있습니다.
- 프로덕션에서는 여러 TaskManager가 여러 머신에 분산되어 있어, 각각 슬롯을 클러스터에 제공합니다.
- JobManager가 어떤 슬롯에서 어떤 job의 어떤 부분을 실행할지 결정합니다.

---

## Docker 기동 전 준비

`src/` 폴더가 반드시 있어야 합니다.  
볼륨 마운트 `./src/:/opt/src`를 사용할 때, 폴더가 없으면 root 권한으로 생성되어 나중에 파일을 만들 때 권한 문제가 발생할 수 있습니다.

```bash
mkdir -p src/job
```

---

## Flink 이미지 빌드 및 전체 서비스 기동

```bash
docker compose up --build -d
```

첫 빌드 시 Python, PyFlink 설치와 커넥터 JAR 다운로드로 몇 분 정도 걸릴 수 있습니다.

---

## 서비스 상태 확인

```bash
docker compose ps
```

**예상 출력 예:**

```
NAME                  IMAGE                           SERVICE        STATUS
workshop-jobmanager   pyflink-workshop                jobmanager     Up
workshop-taskmanager  pyflink-workshop                taskmanager    Up
workshop-postgres     postgres:18                     postgres       Up
workshop-redpanda     redpandadata/redpanda:v25.3.9   redpanda       Up
```

---

## Flink 대시보드 확인

브라우저에서 **http://localhost:8081** 에 접속합니다.  
1개의 TaskManager와 15개의 사용 가능한 task slot이 보여야 합니다.
