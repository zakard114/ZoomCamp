SQL

-- Query public available table (US-central1 Region 기준(데이터 디폴트값))
SELECT station_id, name FROM
    bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;

-- 만약 Access Denied: Table bigquery-public-data:new_york_citibike.citibike_stations:
-- User does not have permission to query table bigquery-public-data:new_york_citibike.citibike_stations, or perhaps it does not exist.
-- 이런 메시지가 뜬다면: 
-- 지금 실행하시려는 **bigquery-public-data**는 미국(US) 리전에 있습니다.

-- 빅쿼리는 설정된 리전과 데이터의 리전이 다르면 "권한이 없거나 데이터가 없다"는 에러를 냅니다.

-- 🛠️ 해결 방법: 리전 설정을 다시 '자동'으로 바꾸기
-- 쿼리 편집기 우측 상단의 [More]/더보기 화살표 버튼 클릭 -> [Query settings]/쿼리 설정 선택.

-- [Additional settings] 항목 아래에 있는 **[Data location]**을 확인하세요.

-- 아까 설정했던 asia-northeast1을 지우고 **Auto-select**로 다시 변경합니다. 내 경우, 그냥 Auto-select 체크박스만 체크.

-- **[Save]**를 누른 후 쿼리를 다시 실행해 보세요.     결과: 작동


-- US-central1 Region 기준(데이터 디폴트값):
-- 위 공용 데이터를 내 프로젝트의 nytaxi 데이터셋으로 복사: 내 프로젝트에 citibike_stations 테이블 만들기
-- 이 쿼리는 공용 데이터를 읽어와서 내 nytaxi 데이터셋에 새로운 테이블로 저장합니다.
-- 이렇게 하면 모든 데이터가 내가 설정한 리전(이 경우 asia-northeast1)에 모이게 되므로, 
-- 리전 설정을 바꿀 필요 없이 Yellow/Green 택시 데이터와 함께 바로 조인(Join)하거나 쿼리할 수 있습니다.
CREATE OR REPLACE TABLE `de-zoomcamp-02-zakard.nytaxi.citibike_stations` AS
SELECT * FROM `bigquery-public-data.new_york_citibike.citibike_stations`;

-- 조회: 
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.citibike_stations` LIMIT 100;



-- 비 US-central1 Region, asia-northeast1 기준 시, cloud shell에 다음 커멘드 입력:
-- 1. 현재 세션에 프로젝트 ID 강제 설정
-- gcloud config set project de-zoomcamp-02-zakard

-- 2. 내 프로젝트에 new_york_citibike 데이터셋 생성 (도쿄 리전)
-- bq --location=asia-northeast1 mk -d de-zoomcamp-02-zakard:new_york_citibike

-- 3. 이미 nytaxi에 복사된 테이블을 새 데이터셋으로 복사
-- bq cp de-zoomcamp-02-zakard:nytaxi.citibike_stations de-zoomcamp-02-zakard:new_york_citibike.citibike_stations

-- 이제 의도하신 대로 별도의 데이터셋에서 조회됩니다.
SELECT * FROM `de-zoomcamp-02-zakard.new_york_citibike.citibike_stations` LIMIT 10;


---------------------------------------------------------
-- 1. 외부 테이블(External Table) 생성 (GCS 참조용)
---------------------------------------------------------
-- Yellow 외부 테이블
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-02-zakard.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://kestra-zoomcamp-zakard-demo/yellow_tripdata_*.csv'],
  skip_leading_rows = 1
);

-- Green 외부 테이블
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-02-zakard.nytaxi.external_green_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://kestra-zoomcamp-zakard-demo/green_tripdata_*.csv'],
  skip_leading_rows = 1
);


---------------------------------------------------------
-- 2. YELLOW TAXI 최적화 (안전 DML 방식)
---------------------------------------------------------
-- (1) 파티션 테이블 구조 생성
CREATE OR REPLACE TABLE `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_partitioned`
PARTITION BY DATE(tpep_pickup_datetime)
AS SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_non_partitioned` WHERE 1=0;

-- (2) 데이터 삽입
INSERT INTO `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_partitioned`
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_non_partitioned`;

-- (3) 파티션 + 클러스터 테이블 구조 생성
CREATE OR REPLACE TABLE `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_partitioned_clustered`
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID
AS SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_non_partitioned` WHERE 1=0;

-- (4) 데이터 삽입
INSERT INTO `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_partitioned_clustered`
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_non_partitioned`;


---------------------------------------------------------
-- 3. GREEN TAXI 최적화 (안전 DML 방식)
---------------------------------------------------------
-- (1) 파티션 테이블 구조 생성
CREATE OR REPLACE TABLE `de-zoomcamp-02-zakard.nytaxi.green_tripdata_partitioned`
PARTITION BY DATE(lpep_pickup_datetime)
AS SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.green_tripdata_non_partitioned` WHERE 1=0;

-- (2) 데이터 삽입
INSERT INTO `de-zoomcamp-02-zakard.nytaxi.green_tripdata_partitioned`
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.green_tripdata_non_partitioned`;

-- (3) 파티션 + 클러스터 테이블 구조 생성
CREATE OR REPLACE TABLE `de-zoomcamp-02-zakard.nytaxi.green_tripdata_partitioned_clustered`
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY VendorID
AS SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.green_tripdata_non_partitioned` WHERE 1=0;

-- (4) 데이터 삽입
INSERT INTO `de-zoomcamp-02-zakard.nytaxi.green_tripdata_partitioned_clustered`
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.green_tripdata_non_partitioned`;


---------------------------------------------------------
-- 4. [최종 확인] 성능 및 메타데이터 조회
---------------------------------------------------------
-- 파티션 정보 요약
SELECT table_name, partition_id, total_rows
FROM `de-zoomcamp-02-zakard.nytaxi.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name LIKE '%_partitioned%'
ORDER BY table_name, partition_id DESC;

-- 파티션 성능 비교 테스트 (   19년 6월 Yellow 데이터)
SELECT DISTINCT(VendorID)
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_non_partitioned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

SELECT DISTINCT(VendorID)
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_partitioned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30';

-- 클러스터링 성능 비교 테스트 (   19년 6월 Yellow 데이터)

-- 1. 파티션 테이블 성능 테스트
SELECT count(*) as trips
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_partitioned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30'
  AND VendorID = 1; -- 세미콜론을 여기로 옮겨야 합니다.

-- 2. 파티션 + 클러스터 테이블 성능 테스트
SELECT count(*) as trips
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_partitioned_clustered`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30'
  AND VendorID = 1;


---


-- 번외
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.external_yellow_tripdata` LIMIT 100;
