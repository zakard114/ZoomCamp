# BigQuery ML Taxi Tip Model을 TensorFlow Serving으로 배포하기

이 문서는 BigQuery ML로 학습한 Taxi Tip 예측 모델을  
GCS에서 추출하여 로컬 환경에서 TensorFlow Serving(Docker)으로 서빙하고,  
REST API를 통해 예측을 수행하는 전체 과정을 설명합니다.

---

## Original Instruction (Reference)

```text
gcloud auth login
bq --project_id taxi-rides-ny extract -m nytaxi.tip_model gs://taxi_ml_model/tip_model
mkdir /tmp/model
gsutil cp -r gs://taxi_ml_model/tip_model /tmp/model
mkdir -p serving_dir/tip_model/1
cp -r /tmp/model/tip_model/* serving_dir/tip_model/1
docker pull tensorflow/serving
docker run -p 8501:8501 --mount type=bind,source=pwd/serving_dir/tip_model,target=/models/tip_model -e MODEL_NAME=tip_model -t tensorflow/serving &
curl -d '{"instances": [...]}' -X POST http://localhost:8501/v1/models/tip_model:predict

----

## 내 버전


Plan A: VS Code Git bash ver.

# 1. Cloud: BQ에서 모델 추출 (이게 먼저!)
bq --project_id de-zoomcamp-02-zakard extract -m de-zoomcamp-02-zakard:nytaxi.tip_model gs://kestra-zoomcamp-zakard-demo/tip_model

# 2. Auth: 로컬 인증 갱신
gcloud auth application-default login

# 3. Local: 폴더 생성
mkdir -p serving_dir/tip_model/1

# 4. Sync: 클라우드 -> 로컬 복사
gcloud storage cp -r gs://kestra-zoomcamp-zakard-demo/tip_model/* serving_dir/tip_model/1/

# 5. Docker: 기존 컨테이너 정리 및 엔진 확보
docker rm -f tf_serving_taxi 2>/dev/null

# 6. TensorFlow Serving 이미지 가져오기
docker pull tensorflow/serving

# 7. Serving: 컨테이너 실행 (Windows 전용 경로 처리)
MSYS_NO_PATHCONV=1 docker run -d -p 8501:8501 \
  --name tf_serving_taxi \
  --mount type=bind,source="//$(pwd)/serving_dir/tip_model",target=/models/tip_model \
  -e MODEL_NAME=tip_model \
  -t tensorflow/serving

# 8. Check: 로그 확인
docker logs tf_serving_taxi

# 9. Test: 예측 호출
curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' \
  -X POST http://localhost:8501/v1/models/tip_model:predict


=========


Plan B: GCS Cloud Shell ver. 

Part 1. 프로젝트 설정 및 모델 추출
1️⃣ GCP 프로젝트 설정 (가장 중요)

이 명령어는 모든 gcloud, bq, gsutil 명령어의 기준 프로젝트를 설정합니다.
가장 먼저 실행해야 합니다.

gcloud config set project de-zoomcamp-02-zakard


결과 예시:

zakard330@cloudshell:~ (de-zoomcamp-02-zakard)$

2️⃣ GCP 인증
gcloud auth login


브라우저가 열리면 인증 코드를 입력합니다.

You are now logged in as [zakard330@gmail.com].
Your current project is [de-zoomcamp-02-zakard].

3️⃣ 환경 변수 설정
export PROJECT_ID="de-zoomcamp-02-zakard"
export BUCKET_NAME="kestra-zoomcamp-zakard-demo"
export MODEL_NAME="tip_model"


프로젝트 설정 재확인:

gcloud config set project $PROJECT_ID

4️⃣ BigQuery ML 모델을 GCS로 추출
bq --project_id $PROJECT_ID extract \
  -m $PROJECT_ID:nytaxi.$MODEL_NAME \
  gs://$BUCKET_NAME/$MODEL_NAME

5️⃣ 로컬 서빙 디렉토리 생성 및 모델 다운로드

TensorFlow Serving은 아래와 같은 디렉토리 구조를 요구합니다.

serving_dir/
└── tip_model/
    └── 1/
        ├── saved_model.pb
        └── variables/


디렉토리 생성:

mkdir -p ~/deploy_test/serving_dir/$MODEL_NAME/1


GCS에서 모델 파일 복사:

gsutil cp -r \
  gs://$BUCKET_NAME/$MODEL_NAME/* \
  ~/deploy_test/serving_dir/$MODEL_NAME/1

6️⃣ 모델 파일 확인
ls -l ~/deploy_test/serving_dir/tip_model/1


saved_model.pb 파일이 보이면 Part 1 완료입니다.

Part 2. TensorFlow Serving(Docker)으로 모델 서빙
1️⃣ 기존 컨테이너 정리 (충돌 방지)
docker rm -f tf_serving_taxi 2>/dev/null

2️⃣ TensorFlow Serving 컨테이너 실행
docker run -p 8501:8501 \
  --name tf_serving_taxi \
  --mount type=bind,source=$HOME/deploy_test/serving_dir/tip_model,target=/models/tip_model \
  -e MODEL_NAME=tip_model \
  -t tensorflow/serving &

3️⃣ 서버 실행 확인

아래와 같은 로그가 출력되면 서버가 정상적으로 실행 중입니다.

Exporting HTTP/REST API at:localhost:8501 ...
Entering the event loop ...


이는 에러가 아니라,
서버가 예측 요청을 기다리고 있는 정상 상태입니다.

Part 3. REST API를 통한 예측 요청
1️⃣ 새 터미널 탭 열기

TensorFlow Serving이 실행 중인 터미널은 그대로 두고,
Cloud Shell에서 새 터미널 탭을 엽니다.

2️⃣ 예측 요청 (curl)
curl -d '{
  "instances": [{
    "passenger_count": 1,
    "trip_distance": 12.2,
    "PULocationID": "193",
    "DOLocationID": "264",
    "payment_type": "2",
    "fare_amount": 20.4,
    "tolls_amount": 0.0
  }]
}' \
-X POST http://localhost:8501/v1/models/tip_model:predict

3️⃣ 예측 결과
{
  "predictions": [
    [-0.13526627684768755]
  ]
}
