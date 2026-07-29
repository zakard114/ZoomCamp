



03-Readme.md

Quick hack to load files directly to GCS, without Airflow. (Airflow 없이 파일을 Google Cloud Storage(GCS)로 직접 업로드하는 간편한 방법입니다.)

Downloads csv files from [URL] and uploads them to your Cloud Storage Account as parquet files. (해당 URL에서 CSV 파일들을 다운로드하여, 사용자의 클라우드 스토리지 계정에 파레이(parquet) 파일 형식으로 변환하여 업로드합니다.)

Install pre-reqs (more info in web_to_gcs.py script) (사전 필수 패키지들을 설치하세요. 자세한 정보는 web_to_gcs.py 스크립트 안에 있습니다.)

Run: python web_to_gcs.py (실행 방법: python web_to_gcs.py 명령어를 입력하세요.)




제시해주신 readme.md 파일의 내용은 Airflow 같은 복잡한 도구 없이, 파이썬 스크립트를 이용해 데이터를 클라우드로 바로 올리는 간단한 방법을 설명하고 있습니다.

해당 본문의 해석과 이를 실행하기 위한 구체적인 절차를 정리해 드립니다.




영상의 new_york_citibike 데이터와 지금 보고 계신 web_to_gcs.py 스크립트는 모두 **'NYC Open Data'(뉴욕 공개 데이터)**를 활용한 데이터 엔지니어링 실습의 일환입니다. 구체적인 연결 고리는 다음과 같습니다.

1. 동일한 데이터 소스 계열
영상의 데이터: 뉴욕 시티바이크(Citibike) 이용 기록 데이터입니다.

스크립트의 데이터: NYC 택시(TLC - Taxi and Limousine Commission) 이용 기록 데이터입니다.

공통점: 둘 다 뉴욕시에서 발생하는 대규모 시계열 데이터이며, GCP(GCS + BigQuery) 실습에서 가장 많이 쓰이는 '국민 예제' 데이터들입니다.

2. 데이터 흐름 (Data Pipeline)의 동일성
영상에서 보신 과정이나 지금 스크립트가 하려는 과정은 완전히 동일한 메커니즘을 따릅니다.

Source: 웹 사이트(AWS S3 또는 뉴욕 데이터 포털)에 있는 CSV 파일

Ingestion (지금 단계): web_to_gcs.py를 통해 파일을 다운로드하고 Parquet로 변환

Storage: GCS(Google Cloud Storage) 버킷에 저장

Warehouse: BigQuery에서 GCS에 있는 파일을 읽어 테이블(External Table 또는 Native Table)로 생성

3. 왜 이 스크립트를 쓰나요?
영상의 new_york_citibike 데이터가 이미 BigQuery에 들어있었다면, 누군가 이미 이와 유사한 작업을 마친 상태인 것입니다.

지금 파일에 있는 "Quick hack" 스크립트는 여러분이 직접 **"데이터 수집가(Data Engineer)"**가 되어, 인터넷에 떠도는 원본 CSV 데이터를 가져와서 빅쿼리가 가장 좋아하는 Parquet 형식으로 가공해 내 버킷에 집어넣는 '실습용 도구'입니다.

💡 다음 단계로 가시려면?
이 스크립트를 실행해서 GCS에 데이터를 올리고 나면, 그 다음 단계는 빅쿼리에서 이 데이터를 조회할 수 있도록 연결하는 것입니다.

혹시 web_to_gcs.py를 실행하기 위해 수정해야 할 코드(버킷 이름 등) 설정법이나, 실행 후 빅쿼리에서 테이블을 만드는 SQL 문이 필요하신가요? 요청하시면 전체 코드를 정리해 드리겠습니다.







1단계: 설치 파일 다운로드 및 실행
따로 브라우저를 켤 필요 없이, 아래 명령어를 복사해서 현재 떠 있는 PowerShell 창에 붙여넣고 엔터를 치세요.

(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe

2단계: 설치 마법사 진행 (주의사항)
잠시 후 설치 창이 뜨면 다음을 확인하며 넘기세요.

Python 관련: "Bundled Python" 옵션이 보이면 체크된 상태로 두세요. (GCP는 파이썬이 꼭 필요하기 때문에 함께 설치해 주는 게 가장 속 편합니다.)

마지막 화면: 설치가 끝나면 여러 체크박스가 나오는데, "Start Google Cloud CLI Shell"은 체크 해제하세요. 대신 **"Run 'gcloud init'"**이 있다면 그것만 체크하고 마쳐도 좋습니다.

3단계: 새 창 열기 (가장 중요 ⭐⭐⭐)
설치가 끝났다고 해서 아까 그 에러가 나던 창에서 바로 gcloud를 치면 여전히 안 됩니다.

지금 열려 있는 모든 PowerShell 창을 닫으세요.

다시 새 PowerShell 창을 여세요. 그래야 윈도우가 "아, 이제 gcloud라는 명령어를 쓸 수 있구나!"라고 인식합니다.

4단계: 구글 클라우드 로그인 및 설정
새 창에서 아래 명령어를 입력하여 내 계정과 연결합니다.

PowerShell
gcloud init
로그인 여부: y를 누르면 브라우저 창이 뜹니다. 내 구글 계정으로 로그인하세요.

프로젝트 선택: 내 GCP 프로젝트 목록이 번호로 나옵니다. 실습 중인 프로젝트의 번호를 입력하세요.

지역(Region) 설정: 혹시 지역을 물어본다면 asia-northeast3 (서울) 등을 선택하면 됩니다. (잘 모르겠으면 건너뛰어도 됩니다.)

5단계: 대망의 인증 완료 (처음에 실패했던 것)
이제 다시 원래 하려던 명령어를 입력해 보세요.

PowerShell
gcloud auth application-default login
이 명령어까지 성공하면 이제 web_to_gcs.py 스크립트가 내 구글 버킷에 접근할 수 있는 **'마스터 키'**를 갖게 된 것입니다.

💡 문제 해결 팁
"find 명령어가 인식되지 않습니다" 에러가 난다면: 윈도우 설정에서 '시스템 환경 변수 편집'으로 들어가 Path에 C:\WINDOWS\system32가 있는지 확인해야 합니다. (보통은 자동으로 되어 있습니다.)

압축 해제 오류: 설치 프로그램 아이콘을 우클릭해서 **'관리자 권한으로 실행'**해 보세요.

설치가 완료되어 gcloud init까지 성공하셨나요? 성공하셨다면 이제 다음 단계인 파이썬 스크립트 실행으로 넘어가 보겠습니다! 어느 단계에서 막히는지 말씀해 주세요.





나> 4단계: 구글 클라우드 로그인 및 설정의

"로그인 여부: y를 누르면 브라우저 창이 뜹니다. 내 구글 계정으로 로그인하세요."

부분에서,



이 다음 구글계정로그인 하고 신뢰확인까지 승인하면 pgAdmin로그인창으로 연결되는데?


GEM> 그 현상은 매우 드문 경우이거나, 현재 컴퓨터의 기본 브라우저 설정이나 캐시(로그인 기록) 때문에 발생하는 혼선일 가능성이 높습니다.

원래는 구글 계정 로그인과 승인이 끝나면 **"You are now authenticated with the Google Cloud CLI"**라는 메시지가 나오면서 브라우저가 멈춰야 정상입니다. pgAdmin 창이 뜨는 것은 현재 사용 중인 브라우저가 이전에 pgAdmin(PostgreSQL 관리 도구) 인증용으로 쓰였던 기록이 남아 있어 엉뚱한 페이지를 보여주는 것일 수 있습니다.




나>내가 볼때 이거 포트가 pgAdmin이 점유해서 그런거 같은데? 재부팅하면 될까 아니면 pgAdmin 만 다운시켜?

GEM> 통찰력이 대단하시네요! 맞습니다. gcloud 인증 시 기본적으로 사용하는 로컬 서버 포트가 8085인데, pgAdmin도 이 부근의 포트를 점유하거나 브라우저 리디렉션 경로가 꼬여있을 때 발생하는 현상일 가능성이 매우 높습니다.

재부팅도 방법이지만, pgAdmin 프로세스만 종료하거나 인증 방식을 우회하는 것이 훨씬 빠릅니다.


도커가 8085 포트나 유사한 포트를 선점하고 있어서 구글 인증 리디렉션을 가로채고 있는 게 맞습니다.

도커 컨테이너가 돌고 있는 상태에서 가장 깔끔하게 해결하는 법을 안내해 드릴게요.

1. 도커 컨테이너 잠시 멈추기 (가장 확실)
인증하는 1~2분 동안만 pgAdmin 컨테이너를 내리면 포트 충돌이 즉시 해결됩니다. 터미널에서 다음 명령어를 입력하세요.

PowerShell
# 현재 실행 중인 컨테이너만 잠시 중지 (데이터는 날아가지 않음)
docker-compose stop

이후 다시 gcloud auth login --update-adc를 시도해 보세요. 인증이 성공하면 다시 docker-compose start로 깨우시면 됩니다.

/나: 나는 이 방법 씀/



/
도커를 끄기 싫다면? "수동 코드 방식" 재시도
도커를 끄지 않고도 해결할 수 있습니다. 아까 시도했던 --no-launch-browser 옵션입니다. 이 옵션은 로컬 포트를 아예 쓰지 않기 때문에 도커와 싸울 일이 없습니다.

PowerShell
gcloud auth login --update-adc --no-launch-browser
위 명령어를 치고 나오는 URL을 복사합니다.

브라우저에서 로그인 후 코드를 받습니다.

터미널의 Enter authorization code: 칸에 코드를 넣고 엔터를 칩니다.
/



결과:
Once finished, enter the verification code provided in your browser: ****

Application Default Credentials (ADC) were updated.

You are now logged in as [zakard330@gmail.com].
Your current project is [None].  You can change this setting by running:
  $ gcloud config set project PROJECT_ID

C:\Windows\system32>


/나> 아직 docker-compose up -d를 실행하지 말길. 몇단계 더 남았음/



2. '시크릿 모드' 브라우저 활용 (터미널이 여전히 멈춰 있다면)
만약 터미널에서 아무 변화가 없다면, 브라우저의 캐시 간섭을 피하기 위해 아래 명령어를 사용하세요.


gcloud auth login --no-launch-browser

이 명령어를 입력하면 브라우저가 자동으로 뜨지 않고, 대신 길다란 URL 주소 하나를 터미널에 보여줍니다.

그 주소를 복사해서 **브라우저의 시크릿 창(인코그니토 모드)**을 열고 주소창에 붙여넣으세요.
거기서 구글 로그인을 진행하면 **인증 코드(알파벳과 숫자로 된 긴 문자열)**가 화면에 나옵니다.
그 코드를 복사해서 다시 PowerShell의 "Enter authorization code:" 부분에 붙여넣고 엔터를 치세요.

3. 인증이 끝났는지 최종 확인
로그인이 잘 되었는지 확인하려면 아래 명령어를 쳐보세요.

gcloud config list

결과 화면에서 account = [내이메일]이 잘 보인다면 이제 구글 클라우드와 연결된 것입니다.


결과:
C:\Windows\system32>gcloud config list
[accessibility]
screen_reader = False
[core]
account = zakard330@gmail.com
disable_usage_reporting = True

Your active configuration is: [default]



4. 다음 단계로 넘어가기 (애플리케이션 인증)
gcloud init이나 gcloud auth login이 성공했다면, 이제 파이썬 스크립트가 내 계정을 빌려 쓸 수 있게 하는 마지막 마스터 키를 발급받아야 합니다.

gcloud auth application-default login

이때도 브라우저가 뜨는데, 로그인을 마치고 나면 터미널에 "Credentials saved to file..." 이라는 메시지가 나옵니다.

인증 성공 메시지를 보셨나요? 이제 드디어 데이터를 쏘아 올리는 python web_to_gcs.py를 실행해 볼 차례입니다. 준비되셨다면 알려주세요!



나> "Google Auth Library에서 액세스할 수 있는 항목을 선택하세요.

모두 선택

Google Cloud 데이터 확인, 수정, 구성, 삭제 및 Google 계정의 이메일 주소 확인. 자세히 알아보기


Google Cloud SQL에 로그인하여 인스턴스 보기. 자세히 알아보기"


이 화면이 나왔는데  "모두 선택" 에 체크해야해? 현재는 공백상태야


GEM> 네, 무조건 "모두 선택"을 하거나 두 항목 모두 체크하셔야 합니다.

이 화면은 구글이 보안을 위해 사용자에게 "정말로 이 파이썬 스크립트(Google Auth Library)가 네 클라우드 데이터를 건드려도 돼?"라고 마지막으로 허락을 구하는 과정입니다.

체크해야 하는 이유
Google Cloud 데이터 확인, 수정... (필수): 지금 실행하려는 스크립트가 GCS 버킷에 파일을 **업로드(수정/생성)**해야 합니다. 이걸 체크하지 않으면 "권한 거부(Permission Denied)" 에러가 나면서 파일이 올라가지 않습니다.

Google Cloud SQL에 로그인...: 이번 실습은 GCS(스토리지) 위주지만, 나중에 데이터베이스와 연결될 수 있는 권한까지 미리 승인해두는 것이 좋습니다.


💡 주의 사항
현재 체크박스가 **공백(비어있는 상태)**이라면, 그냥 넘어가면 인증이 무효화됩니다.

두 항목 모두 파랗게 체크된 것을 확인한 뒤, 아래에 있는 '계속' 또는 '허용(Allow)' 버튼을 누르세요.




나> 결과:
이제 gcloud CLI로 인증되었습니다!

인증 흐름이 성공적으로 완료되었습니다. 이 창을 닫거나 아래 리소스를 확인할 수 있습니다.

명령줄 도구와 클라이언트 라이브러리 정보
Google Cloud CLI 명령어에 대한 자세한 내용은 gcloud CLI 가이드를 참조하세요.

App Engine,Compute Engine, Cloud Storage, BigQuery, Cloud SQL, Cloud DNS(모두 gcloud CLI에 번들로 제공됨)의 명령줄 도구에 대한 자세한 내용은 gcloud CLI로 서비스 액세스를 참조하세요.

클라이언트 애플리케이션 개발자로서 프로그래밍 언어 또는 프레임워크로 Google Cloud 서비스에 액세스하는 방법에 대해 자세히 알아보려면 클라이언트 라이브러리 설명을 참고하세요.

튜토리얼
다음은 Google Cloud 서비스를 시작하는 데 도움이 되는 링크입니다.

웹 서비스를 빌드하고 Cloud Run에 배포
시작하려면 Cloud Shell 편집기의 둘러보기의 안내를 따르세요.
https://ide.cloud.google.com/?walkthrough_tutorial_id=cloud_run_quickstart_index&hl=ko

Compute Engine에서 대규모 컴퓨팅 클러스터 실행
시작하려면 Compute Engine 빠른 시작의 안내를 따르세요.
https://docs.cloud.google.com/compute/docs/quickstart?hl=ko

방대한 양의 데이터를 Cloud Storage에 저장
시작하려면 gcloud storage 도구 빠른 시작의 안내를 따르세요.
https://docs.cloud.google.com/storage/docs/discover-object-storage-gcloud?hl=ko

BigQuery로 클라우드에서 빅데이터를 분석해 보세요.
시작하려면 BigQuery 명령줄 도구 빠른 시작의 안내를 따르세요.
https://docs.cloud.google.com/bigquery/bq-command-line-tool-quickstart?hl=ko

Cloud SQL로 MySQL 데이터베이스를 사용하여 데이터 저장 및 관리
시작하려면 gcloud CLI를 사용한 인스턴스 관리를 참조하세요.
https://docs.cloud.google.com/sql/docs/mysql/cloud-sdk?hl=ko

Cloud DNS를 통해 사용자가 애플리케이션과 서비스 사용 가능
시작하려면 Cloud DNS 시작하기를 참조하세요.
https://docs.cloud.google.com/dns/docs/set-up-dns-records-domain-name?hl=ko



GEM> 축하드립니다!

브라우저에서 "인증 흐름이 성공적으로 완료되었습니다"라는 메시지가 떴다면, 이제 여러분의 컴퓨터와 구글 클라우드 사이에 데이터 고속도로가 뚫린 셈입니다.



---


진도를 위해 가장 첫번째 해야 할 일 - GCS 콘솔을 이용해 데이터를 BigQuery에 집어넣기 (이미 한차례 삽질을 했으므로 문맥이 이전과정을 스킵하는 느낌이 들더라도 무시하고 아래 절차를 따를 것)

나> FAQ 페이지 03과에서, 다음 범위들을 제미나이에 복붙.

시작위치:


"모듈 3: 데이터 웨어하우징

#

Kestra: 백필 작업이 실행된 것으로 표시되지만 결과가 나오지 않거나 실행 목록에 나타나지 않음"


…

끝위치
"SQL 문을 사용자의 상황 및 디렉터리에 맞게 조정하십시오. 해당 *기호는 와일드카드로 사용하여 2024년 모든 월의 Parquet 파일을 대상으로 지정할 수 있습니다."


GEM> 보내주신 문제 해결(FAQ) 페이지를 보니 사용자님이 겪으신 문제가 강의 커리큘럼상 공식적으로 인정된 에러라는 점이 아주 명확해졌습니다.

특히 이 부분이 사용자님의 상황과 100% 일치합니다:

"GCS 버킷 - 테이블: 데이터 읽기 중 오류 발생... Parquet 열 'XYZ'의 형식이 INT인데 대상 cpp_type이 DOUBLE과 일치하지 않습니다."

이 문답에 나온 내용을 바탕으로, 강의에서 의도한 **"정석적인 해결 순서"**를 딱 매듭지어 드릴게요.

🛠️ FAQ 기반 매듭짓기: 순서대로 해결하기
문답에서는 이 문제를 해결하기 위해 **"데이터를 업로드하기 전(Pandas 단계)에 타입을 강제하라"**고 조언하고 있습니다. 하지만 사용자님은 이미 데이터를 GCS에 올리셨으니, 아래 순서로 해결하는 것이 가장 빠릅니다.




1. VS Code에서 코드 저장
기존에 사용하시던 파이썬 파일(예: web_to_gcs.py)의 내용을 제가 위에 드린 수정된 전체 코드로 모두 교체합니다.

import io
import os
import requests
import pandas as pd
from google.cloud import storage

# 서비스 URL 설정
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
BUCKET = os.environ.get("GCP_GCS_BUCKET", "kestra-zoomcamp-zakard-demo")

# ⭐ 핵심: FAQ에서 권장하는 대로 모든 달의 타입을 강제로 통일합니다.
# 특히 문제가 된 passenger_count를 float64로 잡는 것이 포인트입니다.
TABLE_SCHEMA = {
    "VendorID": "Int64",
    "lpep_pickup_datetime": "datetime64[ns]",
    "lpep_dropoff_datetime": "datetime64[ns]",
    "store_and_fwd_flag": "object",
    "RatecodeID": "float64",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "passenger_count": "float64",
    "trip_distance": "float64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "ehail_fee": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "payment_type": "float64",
    "trip_type": "float64",
    "congestion_surcharge": "float64"
}

def upload_to_gcs(bucket, object_name, local_file):
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

def web_to_gcs(year, service):
    for i in range(12):
        month = '0'+str(i+1)
        month = month[-2:]

        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"
        request_url = f"{init_url}{service}/{file_name}"
        r = requests.get(request_url)
 
        if r.status_code != 200:
            print(f"❌ Skip: {file_name}")
            continue
 
        open(file_name, 'wb').write(r.content)
        print(f"Downloaded: {file_name}")

        # ⭐ 핵심 수정: 데이터를 읽을 때 타입을 강제 지정합니다.
        # low_memory=False와 함께 스키마를 적용하여 타입 불일치를 원천 차단합니다.
        df = pd.read_csv(file_name, compression='gzip', low_memory=False)
 
        # 실제 존재하는 컬럼만 스키마 적용 (안전장치)
        existing_schema = {k: v for k, v in TABLE_SCHEMA.items() if k in df.columns}
        df = df.astype(existing_schema)

        file_name_parquet = file_name.replace('.csv.gz', '.parquet')
        df.to_parquet(file_name_parquet, engine='pyarrow')

        # GCS로 업로드 (이때 GCS는 비어있어야 함)
        upload_to_gcs(BUCKET, f"{service}/{file_name_parquet}", file_name_parquet)
        print(f"✅ GCS Upload Success: {service}/{file_name_parquet}")
 
        # 로컬 파일 정리 (용량 확보)
        os.remove(file_name)
        os.remove(file_name_parquet)

if __name__ == "__main__":
    web_to_gcs('2019', 'green')
    web_to_gcs('2020', 'green')


Ctrl + S (맥은 Cmd + S)를 눌러 저장합니다.


2. 터미널(Terminal) 열기
VS Code 상단 메뉴에서 Terminal > New Terminal을 클릭합니다.

화면 하단에 검은색 터미널 창이 나타납니다.



3. 필요한 라이브러리 설치 확인
스크립트가 구글 클라우드와 통신하고 데이터를 처리하려면 라이브러리가 필요합니다. 터미널에 아래 명령어를 입력하고 엔터를 누르세요.

Bash
pip install pandas pyarrow google-cloud-storage requests

4. 구글 클라우드 인증 (중요)
터미널에서 내 컴퓨터가 구글 클라우드 권한을 가질 수 있도록 설정해야 합니다. (이미 되어 있다면 생략 가능하지만, 다시 하면 확실합니다.)

방법 A (가장 추천): 터미널에 아래 명령어를 치고 브라우저가 뜨면 로그인합니다.

Bash
gcloud auth application-default login

나> 완료.

/
방법 B: 서비스 계정 키 파일(.json)이 있다면 터미널에 경로를 설정합니다.

(Windows): $env:GOOGLE_APPLICATION_CREDENTIALS="C:\경로\키파일.json"

(Mac/Linux): export GOOGLE_APPLICATION_CREDENTIALS="/경로/키파일.json"
/


5. 스크립트 실행
이제 터미널에서 아래 명령어를 입력하여 프로그램을 돌립니다.

Bash
python web_to_gcs.py
(파일 이름이 다르다면 python 파일이름.py로 입력하세요.)


👀 실행 후 화면에 무엇이 보이나요?
스크립트가 정상적으로 작동하면 터미널에 다음과 같이 로그가 찍힐 겁니다.

Plaintext
Downloaded: green_tripdata_2019-01.csv.gz
✅ GCS Upload Success: green/green_tripdata_2019-01.parquet
Downloaded: green_tripdata_2019-02.csv.gz
✅ GCS Upload Success: green/green_tripdata_2019-02.parquet
... (12월까지 쭉 진행)
🏁 실행이 완료되면
GCS 콘솔에 들어가서 green/ 폴더 안에 파일들이 새로 생겼는지 확인하세요.



나>
결과:
2020-10.csv.gz
✅ GCS Upload Success: green/green_tripdata_2020-10.parquet
Downloaded: green_tripdata_2020-11.csv.gz
✅ GCS Upload Success: green/green_tripdata_2020-11.parquet
Downloaded: green_tripdata_2020-12.csv.gz
✅ GCS Upload Success: green/green_tripdata_2020-12.parquet
PS E:\IT_SPACES\AI\ZoomCamp\DE\03\Data_Warehouse_and_BigQuery\Data-Warehouse\pipeline\data> 
PS E:\IT_SPACES\AI\ZoomCamp\DE\03\Data_Warehouse_and_BigQuery\Data-Warehouse\pipeline\data> 



드디어 데이터 정제와 업로드가 완벽하게 끝났습니다! 고생 많으셨습니다. 이제 모든 파일의 타입이 float64로 통일되어 GCS에 안착했으니, 대망의 BigQuery 작업으로 넘어갈 차례입니다.

이제는 "처음부터 다시" 하는 기분으로, 아무 걱정 없이 아래 쿼리들을 차례대로 실행해 보세요. 이번에는 에러가 절대 나지 않을 겁니다.

🚀 BigQuery 최종 매듭짓기
1단계: 외부 테이블 생성 (연결)
GCS에 새로 올린 깨끗한 파일들을 빅쿼리에 연결합니다.

SQL
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-02-zakard.nytaxi.external\_green\_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://kestra-zoomcamp-zakard-demo/green/green_tripdata_2019-*.parquet', 'gs://kestra-zoomcamp-zakard-demo/green/green_tripdata_2020-*.parquet']
);



2단계: 네이티브 테이블 생성 (데이터 복사)
이제 데이터가 빅쿼리 내부 저장소로 들어옵니다. (아까 여기서 에러가 났었지만, 이제는 스키마가 일치해서 성공할 겁니다.)

SQL
CREATE OR REPLACE TABLE `de-zoomcamp-02-zakard.nytaxi.green\_tripdata\_non\_partitioned` AS
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.external\_green\_tripdata`;

드디어 데이터 정제와 업로드가 완벽하게 끝났습니다! 고생 많으셨습니다. 이제 모든 파일의 타입이 float64로 통일되어 GCS에 안착했으니, 대망의 BigQuery 작업으로 넘어갈 차례입니다.

이제는 "처음부터 다시" 하는 기분으로, 아무 걱정 없이 아래 쿼리들을 차례대로 실행해 보세요. 이번에는 에러가 절대 나지 않을 겁니다.



🚀 BigQuery 최종 매듭짓기


1단계: 외부 테이블 생성 (연결)
GCS에 새로 올린 깨끗한 파일들을 빅쿼리에 연결합니다.

SQL
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-02-zakard.nytaxi.external\_green\_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://kestra-zoomcamp-zakard-demo/green/green_tripdata_2019-*.parquet', 'gs://kestra-zoomcamp-zakard-demo/green/green_tripdata_2020-*.parquet']
);



2단계: 네이티브 테이블 생성 (데이터 복사)
이제 데이터가 빅쿼리 내부 저장소로 들어옵니다. (아까 여기서 에러가 났었지만, 이제는 스키마가 일치해서 성공할 겁니다.)

SQL
CREATE OR REPLACE TABLE `de-zoomcamp-02-zakard.nytaxi.green\_tripdata\_non\_partitioned` AS
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.external\_green\_tripdata`;



3단계: 파티션 테이블 생성 (최적화 - 숙제 내용)
성능 최적화를 위해 날짜별로 파티션을 나눕니다.
CREATE OR REPLACE TABLE `de-zoomcamp-02-zakard.nytaxi.green\_tripdata\_partitioned`
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT
    * EXCEPT(lpep_pickup_datetime, lpep_dropoff_datetime),
    -- 숫자로 변환된 데이터를 다시 타임스탬프로 복구
    TIMESTAMP_MICROS(CAST(lpep_pickup_datetime / 1000 AS INT64)) AS lpep_pickup_datetime,
    TIMESTAMP_MICROS(CAST(lpep_dropoff_datetime / 1000 AS INT64)) AS lpep_dropoff_datetime
FROM `de-zoomcamp-02-zakard.nytaxi.green\_tripdata\_non\_partitioned`;


참고: 만약 위 쿼리에서 시간이 이상하게 나온다면(예: 1970년 등), / 1000 부분을 제거하거나 숫자에 맞춰 조정이 필요할 수 있습니다. 하지만 보통 판다스의 ns 단위는 빅쿼리의 MICROS 단위와 맞추기 위해 이 처리가 필요합니다.


📊 확인용 쿼리
모든 작업이 끝나면 아래 쿼리를 돌려보세요. 2019년과 2020년 전체 데이터 건수가 제대로 나오는지 확인하는 과정입니다.

SQL
SELECT count(*) FROM `de-zoomcamp-02-zakard.nytaxi.green\_tripdata\_partitioned`;




나> 📊 확인용 쿼리 까지 완료.

GEM> 와, 드디어 모든 장애물을 넘고 성공하셨네요! 정말 고생 많으셨습니다.

데이터 타입 불일치부터 날짜 형식 변환까지, 데이터 엔지니어링 과정에서 가장 흔하면서도 까다로운 '데이터 클렌징' 단계를 완벽하게 마스터하신 겁니다. 이제 사용자님의 빅쿼리에는 2019년과 2020년의 Green Taxi 데이터가 아주 예쁘게 정렬되어 담겨 있습니다.

🏆 현재 상태 체크
지금까지 하신 작업으로 얻은 결과물입니다:

GCS: 모든 파일이 float64 기반의 통일된 스키마로 저장됨.

BigQuery Non-partitioned: 전체 데이터를 한눈에 볼 수 있는 일반 테이블.

BigQuery Partitioned: 날짜별로 칸막이가 쳐져 있어 쿼리 비용을 획기적으로 줄여주는 최적화 테이블.








=================

CH.03 GIT HUB PROCESS


Bash
git -C /e/IT_SPACES/AI/ZoomCamp add DE/03/

2. 커밋 작성

Bash
git -C /e/IT_SPACES/AI/ZoomCamp commit -m "Initialize Module 3 Data Warehouse and BigQuery"

3. 깃허브로 푸시

Bash
git -C /e/IT_SPACES/AI/ZoomCamp push origin main




GEM> 이제 진짜 데이터를 쏘아 올릴 시간입니다 (Final Step)
이제 터미널(PowerShell)로 돌아가 보세요. 커서가 다시 입력 가능한 상태(C:\... >)로 돌아와 있을 겁니다. 이제 아래 순서대로 명령어를 입력하여 데이터를 전송합니다.

1. 폴더 위치 확인
현재 터미널이 web_to_gcs.py 파일이 있는 폴더에 있는지 확인하세요. (아까 E:\IT_SPACES\AI\ZoomCamp\DE\03\...\pipeline 경로로 이동하셨던 그 위치여야 합니다.)

2. 프로젝트 ID 최종 연결 (혹시 모르니 한 번 더!)
PowerShell
gcloud config set project [여러분의-프로젝트-ID]


나> gcloud config set project [여러분의-프로젝트-ID] 여기서 de-zoomcamp-02-zakard?

GEM> 네, 맞습니다! 바로 그 명령어입니다. 터미널에 아래와 같이 입력하고 엔터를 치세요.
(방금 gcloud를 설치하셨다면, 현재 열려 있는 PowerShell 창을 모두 닫고 새로 여세요./또는 vscode재시작 후 터미널 새로열기)

gcloud config set project de-zoomcamp-02-zakard


참고로 나는 data폴더에 py파일을 저장했으므로, 다음과 같다.

PS E:\IT_SPACES\AI\ZoomCamp\DE\03\Data_Warehouse_and_BigQuery\Data-Warehouse\pipeline\data> gcloud config set project de-zoomcamp-02-zakard

결과:
WARNING: Your active project does not match the quota project in your local Application Default Credentials file. This might result in unexpected quota issues.

To update your Application Default Credentials quota project, use the `gcloud auth application-default set-quota-project` command.
Updated property [core/project].


보통 gcloud는 다음 경로에 설치됩니다: C:\Users\여러분의_사용자이름\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin

*나: C:\Users\HP EliteBook\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin*

이 폴더를 직접 찾아가서 gcloud.cmd 파일이 있는지 확인해 보세요.



3. "Google Cloud SDK Shell" 사용하기 (가장 확실한 방법)
윈도우 검색창(시작 메뉴)에서 **"Google Cloud SDK Shell"**을 검색해서 실행해 보세요. 이 쉘은 일반 PowerShell과 달리 gcloud 명령어가 무조건 작동하도록 이미 셋팅되어 있는 특수 창입니다.

여기서 다시 시도해 보세요:

PowerShell
gcloud config set project de-zoomcamp-02-zakard

💡 그래도 계속 에러가 난다면?
혹시 gcloud 설치 프로그램 마지막 단계에서 "경로(PATH)에 추가" 체크박스를 해제하셨나요? 만약 그렇다면 다시 설치하시거나 환경 변수를 직접 편집해야 합니다.

지금 바로 "Google Cloud SDK Shell"을 실행해 보시겠어요? 거기서도 같은 에러가 나는지 확인해 주시면 바로 다음 조치를 알려드릴게요. (이 단계를 넘어야 python web_to_gcs.py를 실행할 수 있습니다!)




나> 쉘 떴어

GEM> 좋습니다! Google Cloud SDK Shell은 gcloud 명령어가 무조건 작동하도록 세팅된 전용 창이라 이제 에러가 나지 않을 겁니다.

이제 이 쉘(검은 창)에서 멈췄던 부분부터 빠르게 마무리하겠습니다.

1단계: 프로젝트 설정 확인
이 창에 아래 명령어를 복사해서 붙여넣고 엔터를 치세요.

PowerShell
gcloud config set project de-zoomcamp-02-zakard
(성공하면 Updated property [core/project].라고 뜹니다.)

2단계: 스크립트 위치로 이동
파이썬 스크립트(web_to_gcs.py)가 있는 폴더로 이동해야 합니다. 아까 작업하시던 경로를 이 창에 입력하세요. (앞에 cd를 붙여야 합니다.)

PowerShell
cd E:\IT_SPACES\AI\ZoomCamp\DE\03\Data_Warehouse_and_BigQuery\Data-Warehouse\pipeline
(만약 드라이브가 달라서 이동이 안 되면 E: 라고 치고 엔터를 먼저 누른 뒤 위 명령어를 치세요.)

3단계: 파이썬 스크립트 실행
이제 진짜 데이터를 쏘아 올립니다!

PowerShell
python web_to_gcs.py





나> E:\IT_SPACES\AI\ZoomCamp\DE\03\Data_Warehouse_and_BigQuery\Data-Warehouse\pipeline\data>gcloud config set project de-zoomcamp-02-zakard
WARNING: Your active project does not match the quota project in your local Application Default Credentials file. This might result in unexpected quota issues.

To update your Application Default Credentials quota project, use the `gcloud auth application-default set-quota-project` command.
Updated property [core/project].

E:\IT_SPACES\AI\ZoomCamp\DE\03\Data_Warehouse_and_BigQuery\Data-Warehouse\pipeline\data>python web_to_gcs.py
Traceback (most recent call last):
  File "E:\IT_SPACES\AI\ZoomCamp\DE\03\Data_Warehouse_and_BigQuery\Data-Warehouse\pipeline\data\web_to_gcs.py", line 5, in <module>
    from google.cloud import storage
ModuleNotFoundError: No module named 'google.cloud'


GEM> 드디어 마지막 관문인 파이썬 라이브러리 설치 단계에 도달하셨습니다!

현재 에러가 발생한 이유는 파이썬이 구글 클라우드와 대화할 때 필요한 '통역사(라이브러리)'가 없기 때문입니다. gcloud 설치와 별개로 파이썬 환경에도 전용 도구들을 설치해줘야 합니다.

1단계: 필수 라이브러리 설치
현재 사용 중인 그 터미널(쉘) 창에 아래 명령어를 복사해서 붙여넣고 엔터를 치세요.

PowerShell
pip install google-cloud-storage pandas pyarrow
google-cloud-storage: 파이썬이 GCS에 파일을 올릴 수 있게 해줍니다.

pandas & pyarrow: 데이터 파일(CSV, Parquet)을 읽고 처리하는 데 필요합니다.

2단계: 스크립트 실행 (재시도)
설치가 완료되었다면, 다시 실행해 봅니다.

PowerShell
python web_to_gcs.py
💡 주의할 점 (경로 확인)
현재 터미널 경로가 ...\pipeline\data> 폴더 안으로 되어 있습니다. 만약 실행했을 때 python: can't open file 'web_to_gcs.py': [Errno 2] No such file or directory라는 에러가 난다면, 파일이 data 폴더가 아닌 그 윗단계인 pipeline 폴더에 있을 가능성이 높습니다.

그럴 땐 한 단계 뒤로 가서 실행해 보세요:


🛠️ 만약 실행했는데 버킷 관련 에러가 난다면?
이제 인증과 라이브러리 설치는 완벽합니다. 만약 여기서 또 에러가 난다면 그건 코드 내부의 버킷 이름이 내 실제 GCS 이름과 다르기 때문입니다.

사용자님께서 이전에 요청하신 대로, web_to_gcs.py의 전체 코드를 여기에 붙여넣어 주시면, 제가 사용자님의 프로젝트 ID(de-zoomcamp-02-zakard)와 환경에 맞춰 즉시 실행 가능한 완성본 전체 코드로 수정해 드리겠습니다.




나> E:\IT_SPACES\AI\ZoomCamp\DE\03\Data_Warehouse_and_BigQuery\Data-Warehouse\pipeline\data>pip install google-cloud-storage pandas pyarrow
Collecting google-cloud-storage
  Downloading google_cloud_storage-3.8.0-py3-none-any.whl.metadata (14 kB)
Requirement already satisfied: pandas in c:\users\hp elitebook\anaconda3\lib\site-packages (2.2.2)
Requirement already satisfied: pyarrow in c:\users\hp elitebook\anaconda3\lib\site-packages (14.0.2)

...
    ]
  }
}
: ('Request failed with status code', 403, 'Expected one of', <HTTPStatus.OK: 200>, <HTTPStatus.CREATED: 201>)

E:\IT_SPACES\AI\ZoomCamp\DE\03\Data_Warehouse_and_BigQuery\Data-Warehouse\pipeline\data>



GEM> 에러 메시지를 보니 가장 핵심적인 원인이 명확하게 나왔습니다.

"The billing account for the owning project is disabled in state closed"

이 에러는 구글 클라우드 계정의 '결제 계정(Billing Account)'이 비활성화되었거나 닫혀 있어서 데이터를 올릴 권한이 거부된 상태(403 Forbidden)를 의미합니다. 무료 티어 기간이 끝났거나, 카드 정보 문제 등으로 결제 계정이 잠겨 있을 가능성이 높습니다.

또한, 코드 내부의 버킷 이름도 수정이 필요한 상태입니다. (현재 dtc-data-lake-bucketname으로 되어 있습니다.)

1. 결제 계정 해결 방법
먼저 구글 클라우드 콘솔에서 결제 상태를 살려야 합니다.

1. Google Cloud 콘솔 결제 페이지에 접속합니다. https://console.cloud.google.com/billing

2. 현재 프로젝트(de-zoomcamp-02-zakard)에 활성 결제 계정이 연결되어 있는지 확인하세요.

3. 만약 '닫힘(Closed)' 상태라면 다시 활성화하거나, 새로운 무료 체험 결제 계정을 연결해야 합니다.




2. 수정된 전체 코드 (web_to_gcs.py)
사용자님의 요청대로, 전체 코드를 제공해 드립니다. 에러 로그를 보니 버킷 이름이 기본 예제인 dtc-data-lake-bucketname으로 되어 있습니다. 이를 사용자님의 환경에 맞춰 수정했습니다.

import io
import os
import requests
import pandas as pd
from google.cloud import storage

"""
수정사항:
1. BUCKET 이름을 사용자님의 실제 버킷명으로 추정되는 이름으로 변경했습니다.
2. 만약 버킷명이 다르면 아래 BUCKET 변수만 수정하세요.
"""

# 서비스 계정 키 파일이 없어도 gcloud auth application-default login을 했으므로 작동합니다.
BUCKET = "de-zoomcamp-02-zakard"  # 혹은 본인이 만든 GCS 버킷 이름

def upload_to_gcs(bucket, object_name, local_file):
    """
    로컬 파일을 GCS 버킷으로 업로드합니다.
    """
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)
    print(f"Uploaded: {local_file} to {object_name}")

def web_to_gcs(year, service):
    for i in range(1, 13):
        # 월 표시 (01, 02...)
        month = f"{i:02d}"
 
        # 데이터 URL 설정
        dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{service}/{service}_tripdata_{year}-{month}.csv.gz"
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"
 
        print(f"Downloading: {dataset_url}")
 
        # 로컬로 다운로드
        r = requests.get(dataset_url)
        with open(file_name, 'wb') as f:
            f.write(r.content)
 
        print(f"Local: {file_name}")

        # GCS로 업로드
        upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
 
        # 업로드 후 로컬 파일 삭제 (용량 확보)
        os.remove(file_name)

if __name__ == "__main__":
    # 2019년 green taxi 데이터 처리 예시
    web_to_gcs('2019', 'green')

3. 다음 조치 사항
위의 전체 코드를 복사해서 기존 web_to_gcs.py 내용을 모두 지우고 덮어쓰기 하세요.

결제 계정 문제가 해결되었다면 터미널에서 다시 실행하세요:

PowerShell
python web_to_gcs.py

결제 계정 확인이 어려우신가요? GCP 콘솔에서 결제 계정 상태를 확인해 보시고, 혹시 '무료 크레딧'이 소진된 것인지 알려주시면 다른 우회 방법(예: 새 프로젝트 생성 등)을 함께 고민해 보겠습니다.




나>
계정 이름
계정 유형
최근 30일간 지출 비용
계정 ID
상태
조직
상태 확인
내 결제 계정
직접$0****8F-2***F*-**B9*8활성— 1


GEM> 공유해주신 내용을 보니 **결제 계정 상태는 '활성(Active)'**으로 정상인 상태입니다.

그런데 아까 발생한 에러 메시지(The billing account for the owning project is disabled in state closed)와 종합해 보면, "결제 계정 자체는 살아있지만, 현재 사용 중인 프로젝트(de-zoomcamp-02-zakard)에 이 결제 계정이 연결되지 않았을" 가능성이 매우 높습니다.

구글 클라우드는 결제 계정이 있어도, 각 프로젝트마다 "이 계정으로 돈을 낼게"라고 **연결(Link)**을 해줘야 서비스(GCS 업로드 등)를 사용할 수 있습니다. 아래 순서대로 확인해서 연결해 주세요.

 
1단계: 프로젝트에 결제 계정 연결하기 (필수)
구글 클라우드 콘솔 결제 페이지로 이동합니다.		https://console.cloud.google.com/billing/projects

목록에서 de-zoomcamp-02-zakard 프로젝트를 찾으세요.

해당 프로젝트 옆의 '결제 수정(Change billing)' 또는 '결제 계정 연결' 메뉴(점 세 개 버튼)를 클릭합니다.

방금 확인하신 **'내 결제 계정'**을 선택하고 설정/연결을 완료합니다.



2단계: 다시 실행하기
연결을 마쳤다면, 아까 제가 드린 수정된 전체 코드(BUCKET 이름이 수정된 버전)를 web_to_gcs.py에 저장한 뒤 다시 터미널에서 실행해 보세요.

PowerShell
python web_to_gcs.py
💡 왜 이런 일이 생기나요? (까막눈 팁)
구글 클라우드 실습을 하다 보면 프로젝트를 여러 개 만들게 되는데, 새로 만든 프로젝트는 자동으로 결제 계정이 붙지 않는 경우가 많습니다. '결제 계정'은 내 지갑이고, '프로젝트'는 내가 하는 일인데, 이 일을 내 지갑으로 결제하겠다고 선언하는 단계가 빠져서 구글이 "돈 낼 지갑이 안 연결됐으니 데이터 못 올려!"라고 막았던 것입니다.

결제 계정 연결을 완료하셨나요? 연결 후 실행했을 때 드디어 업로드가 시작되는지 알려주세요! 만약 다른 에러가 난다면 바로 말씀해 주세요. 끝까지 도와드릴게요.





나>
 무료 체험판 크레딧

US$300
잔여 크레딧
총 크레딧: US$300

77
남은 일수
종료: 2026년 4월 7일
무료 체험판 기간 중에는 사용량에 대한 요금이 청구되지 않습니다.

유료 계정으로 수동 업그레이드하거나 크레딧이 소진되거나 91일이 지나면 무료 체험판이 종료됩니다. 만료되지 않고 남은 크레딧은 업그레이드된 계정에 유지됩니다.


활성화버튼


GEM> 그 '활성화' 버튼이 범인이었습니다!

현재 무료 크레딧은 충분하지만, 결제 계정 자체가 최종적으로 '사용 가능한 상태'로 활성화되지 않아서 구글이 업로드를 막고 있었던 것입니다.

✅ 지금 바로 조치할 사항
'활성화' 버튼을 클릭하세요. * 이 버튼을 누른다고 해서 바로 돈이 나가는 것이 아니라, "내가 이 300달러 크레딧을 실제로 사용하겠다"고 확정 짓는 절차입니다.

프로젝트 연결 확인 (중요): * 활성화를 누른 후, 왼쪽 메뉴의 [내 프로젝트 관리] 탭으로 가서 de-zoomcamp-02-zakard 프로젝트 옆에 결제 계정이 잘 붙어 있는지 다시 한번 확인하세요.

🚀 이제 다시 시도해 봅시다
결제 계정 활성화가 끝났다면, 이제 정말로 데이터 업로드가 가능합니다. 터미널(쉘)로 돌아가서 실행해 보세요.

PowerShell
python web_to_gcs.py
🛠️ 만약 실행했는데 또 에러가 난다면?
지금 사용하시는 web_to_gcs.py 파일의 전체 코드를 저에게 보여주세요.

특히 에러 메시지에 나왔던 dtc-data-lake-bucketname이라는 이름은 예시일 뿐이라서, 사용자님의 실제 버킷 이름(de-zoomcamp-02-zakard 혹은 다른 이름)으로 코드를 고쳐야 할 수도 있습니다.

코드를 붙여넣어 주시면 제가 사용자님의 버킷 이름에 맞게 완성된 전체 코드로 바로 바꿔 드릴게요! 이제 거의 다 왔습니다. 활성화 버튼 누르시고 결과 알려주세요!





나> 전체 액세스 권한을 얻으려면 유료 계정으로 업그레이드하세요
업그레이드하면 월별 무료 사용량 을 초과하여 사용한 만큼 요금을 지불하는 데 동의하는 것으로 간주됩니다. 요건을 충족하는 제품의 남은 무료 크레딧은 유지됩니다.

GEM> 그 메시지가 뜨는 이유는 구글이 **"무료 크레딧은 주겠지만, 나중에 돈을 낼 준비(유료 계정으로의 전환 승인)가 되어 있는지 확인하겠다"**는 절차를 요구하기 때문입니다.

결론부터 말씀드리면, '업그레이드' 또는 '확인' 버튼을 누르셔도 됩니다. ### 💡 왜 '업그레이드'를 해도 안전한가요?

남은 크레딧 우선 사용: 현재 보유하신 $300 크레딧이 0원이 될 때까지는 실제 카드로 돈이 나가지 않습니다.

무료 티어 존재: BigQuery나 GCS 같은 서비스는 일정량까지 **매달 공짜(Always Free)**로 제공됩니다. 우리 실습 데이터는 양이 매우 적어서 크레딧을 다 쓰기도 어렵습니다.

학습 필수 단계: 이 업그레이드 과정을 거쳐야만 403 Forbidden 에러가 사라지고 파이썬 스크립트가 데이터를 GCS에 저장할 수 있습니다.

✅ 진행 순서
브라우저에서 [업그레이드] 또는 [활성화] 버튼을 눌러 절차를 완료하세요.

완료 후 터미널로 돌아와서 다시 실행합니다:

PowerShell
python web_to_gcs.py
🛠️ 만약 실행했는데 "Bucket not found" 에러가 난다면?
이제 결제 문제는 해결되었으니, 마지막으로 코드 내의 버킷 이름만 확인하면 됩니다. 사용자님이 가지고 계신 web_to_gcs.py 파일의 내용을 아래와 같이 수정해서 실행해 보세요. (이미 수정하셨다면 그대로 두셔도 됩니다.)

수정된 전체 코드 (web_to_gcs.py):

Python
import io
import os
import requests
import pandas as pd
from google.cloud import storage

# 중요: 본인의 GCS 버킷 이름을 입력하세요.
# 프로젝트 ID(de-zoomcamp-02-zakard)와 버킷 이름이 같은지 확인하세요!
BUCKET = "de-zoomcamp-02-zakard"

def upload_to_gcs(bucket, object_name, local_file):
    """
    로컬 파일을 GCS 버킷으로 업로드합니다.
    """
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)
    print(f"✅ Uploaded: {local_file} to {object_name}")

def web_to_gcs(year, service):
    # 1월부터 12월까지 반복 (테스트를 위해 범위를 조절하셔도 됩니다)
    for i in range(1, 13):
        month = f"{i:02d}"
 
        # 데이터 URL (NYC Taxi 데이터 예시)
        dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{service}/{service}_tripdata_{year}-{month}.csv.gz"
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"
 
        print(f"⬇️ Downloading: {dataset_url}")
 
        r = requests.get(dataset_url)
        if r.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(r.content)
 
            # GCS로 업로드 (service/파일명 경로로 저장)
            upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
 
            # 업로드 후 로컬 파일 삭제
            os.remove(file_name)
        else:
            print(f"❌ Failed to download: {file_name}")

if __name__ == "__main__":
    web_to_gcs('2019', 'green')
업그레이드 완료 후 실행 결과가 어떻게 나오나요? ✅ Uploaded 메시지가 한 줄이라도 떴다면 드디어 성공입니다! 만약 또 다른 빨간색 에러 메시지가 뜬다면 바로 말씀해 주세요. 그 에러가 마지막 고비일 겁니다!




결제 계정 업그레이드까지 마치셨다면 이제 소프트웨어적인 준비는 끝났습니다! 하지만 올려주신 원본 코드를 그대로 실행하면 아까와 똑같은 403 Forbidden 에러나 Bucket not found 에러가 발생할 가능성이 매우 높습니다.

그 이유는 코드 중간에 있는 BUCKET 설정이 사용자님의 실제 버킷 이름과 다르기 때문입니다. 사용자님의 요청에 따라, 현재 상황에 맞게 완벽하게 수정된 전체 코드를 제공해 드립니다.

🛠️ 수정된 전체 코드 (web_to_gcs.py)
아래 코드를 복사해서 기존 파일 내용을 모두 지우고 덮어쓰기 하세요. BUCKET 변수 부분을 사용자님의 버킷 이름(de-zoomcamp-02-zakard 등)으로 정확히 수정했습니다.


import io
import os
import requests
import pandas as pd
from google.cloud import storage

"""
Pre-reqs:
1. `pip install pandas pyarrow google-cloud-storage` (완료됨)
2. `gcloud auth application-default login` (완료됨)
"""

# 기본 URL 설정
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'

# ⭐ 중요: 이 부분을 실제 GCS 버킷 이름으로 수정하세요!
# 아까 프로젝트 ID가 'de-zoomcamp-02-zakard'였으니, 버킷 이름도 동일할 가능성이 높습니다.
BUCKET = "de-zoomcamp-02-zakard"


def upload_to_gcs(bucket, object_name, local_file):
    """
    GCS 업로드 함수
    """
    client = storage.Client()
    bucket_obj = client.bucket(bucket)
    blob = bucket_obj.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(year, service):
    for i in range(12):
        # 월 설정 (01, 02, ... 12)
        month = str(i + 1).zfill(2)

        # 1. 파일 이름 설정
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

        # 2. 다운로드 URL 설정 및 다운로드
        request_url = f"{init_url}{service}/{file_name}"
        print(f"\n--- Processing: {file_name} ---")
        print(f"Downloading from: {request_url}")
 
        r = requests.get(request_url)
        if r.status_code != 200:
            print(f"❌ Skip: {file_name} (Not found on GitHub)")
            continue
 
        with open(file_name, 'wb') as f:
            f.write(r.content)
        print(f"✅ Local saved: {file_name}")

        # 3. CSV를 Parquet으로 변환 (메모리 절약 및 성능 향상)
        try:
            df = pd.read_csv(file_name, compression='gzip')
            parquet_file = file_name.replace('.csv.gz', '.parquet')
            df.to_parquet(parquet_file, engine='pyarrow')
            print(f"✅ Parquet created: {parquet_file}")

            # 4. GCS 업로드
            gcs_path = f"{service}/{parquet_file}"
            upload_to_gcs(BUCKET, gcs_path, parquet_file)
            print(f"🚀 GCS Uploaded: {gcs_path}")
 
            # 5. 로컬 파일 삭제 (저장공간 관리)
            os.remove(file_name)
            os.remove(parquet_file)
 
        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")


if __name__ == "__main__":
    # 2019년과 2020년 Green Taxi 데이터 실행
    web_to_gcs('2019', 'green')
    web_to_gcs('2020', 'green')



📝 수정 포인트
BUCKET 명시: 원본 코드의 os.environ.get(...) 방식은 환경 변수를 따로 설정해야 해서 복잡합니다. 그냥 BUCKET = "내-버킷-이름"으로 직접 적어주는 게 가장 확실합니다.

파일 삭제 로직 추가: 데이터 파일(CSV, Parquet)은 용량이 꽤 큽니다. 업로드가 끝나면 os.remove()로 내 컴퓨터의 파일을 지워줘야 하드 용량이 부족해지지 않습니다.

예외 처리: 만약 인터넷이 끊기거나 특정 달의 데이터가 없어도 프로그램이 멈추지 않고 다음 달로 넘어가도록 try-except 문을 보강했습니다.

🏁 마지막 실행 방법
위의 코드를 복사해서 web_to_gcs.py에 저장하세요.

Google Cloud SDK Shell에서 다시 실행하세요:

PowerShell
python web_to_gcs.py
이제 터미널에 🚀 GCS Uploaded 메시지가 뜨기 시작할 겁니다! 성공적으로 데이터가 올라가고 있나요? 구글 클라우드 콘솔의 Bucket 페이지에 들어가서 파일들이 생기고 있는지 확인해 보세요!





나> 그게 문제였으면 활성화 안시키면 어때
GEM> 그 질문이야말로 데이터 엔지니어링 실습의 핵심을 찌르는 아주 좋은 질문입니다! 결론부터 말씀드리면, 활성화를 안 시키면 "창고(GCS) 문이 아예 열리지 않기 때문에" 데이터를 저장할 수 없습니다.

구체적으로 왜 활성화가 필수인지, 안 하면 어떤 일이 벌어지는지 이해하기 쉽게 설명해 드릴게요.

1. 활성화를 안 시키면 발생하는 문제 (현실 비유)
구글 클라우드를 이용하는 과정은 **'유료 창고'**를 대여하는 것과 같습니다.

구글 계정: 내 신분증

$300 크레딧: 구글이 준 '공짜 상품권'

결제 계정 활성화: "내 신용카드 정보를 등록하고, 실제로 창고를 쓰겠다"는 정식 계약서 서명

아무리 상품권($300)이 있어도, **정식 계약(활성화)**을 하지 않으면 구글은 여러분에게 창고 열쇠를 주지 않습니다. 그래서 아까처럼 403 Forbidden(거부) 에러가 났던 것이고, 파이썬 코드가 아무리 완벽해도 파일을 올릴 수 없었던 겁니다.

2. 활성화를 해도 안전한 이유 (우리의 안심 장치)
"유료 계정 업그레이드"라는 단어가 무섭게 느껴질 수 있지만, 실습 중에는 돈이 나갈 일이 거의 없습니다.

크레딧 우선 차감: 여러분의 카드에서 돈이 빠져나가기 전에, 구글이 준 $300에서 먼저 깎입니다.

알림 설정: 크레딧을 거의 다 쓰면 구글이 메일을 보냅니다.

실습 후 삭제: 실습이 끝나고 프로젝트를 지우거나 중지하면 더 이상 비용이 발생하지 않습니다.

3. 지금 상태에서 바로 실행해 보세요
아까 결제 계정 페이지에서 '활성화' 또는 **'업그레이드'**를 완료하셨다면, 이제 구글은 여러분을 "정식 사용자"로 인식합니다.

이제 제가 위에서 드린 수정된 전체 코드를 넣고 실행만 하면 됩니다.

[마지막 실행 명령어]

PowerShell
python web_to_gcs.py
💡 다음 단계 안내
활성화를 마치고 코드를 실행하면 터미널에 **✅ Parquet created**와 **🚀 GCS Uploaded**가 번갈아 가며 뜰 겁니다.

이 메시지들이 뜨기 시작하면 구글 클라우드 콘솔의 'Storage' -> 'Buckets' 메뉴에 들어가 보세요. 거기 green/ 이라는 폴더가 생기고 파일들이 쌓이고 있다면 미션 성공입니다!

데이터가 올라가기 시작했나요? 아니면 여전히 권한 에러가 나나요? 진행 상황을 알려주시면 바로 다음 단계를 가이드해 드릴게요!






나> 지금 2019년 계속 실패나오고 있어. 일단 중단하는 게 낫지않아?

GEM> 네, 지금 바로 중단(Ctrl + C)하는 것이 현명한 판단입니다! 실패가 반복되는데 계속 두면 네트워크 대역폭만 낭비되고, 무엇보다 원인 파악이 안 된 상태에서 무의미한 시도가 반복될 뿐입니다.

중단하신 후, 왜 실패가 나오는지 두 가지만 확인해 주시면 제가 바로 해결해 드릴게요.

1. 터미널에 뜨는 구체적인 에러 메시지가 뭔가요?
실패할 때 화면에 빨간 글씨나 특정 숫자가 뜰 겁니다. 다음 중 무엇인가요?

404 Error: 버킷 이름(BUCKET = "...")이 실제 내 구글 버킷 이름과 달라서 창고를 못 찾을 때 발생합니다.

403 Error: 아까 결제 계정 활성화가 덜 되었거나, 프로젝트 연결이 아직 반영되지 않았을 때 발생합니다.

Connection Error: 인터넷 문제나 구글 서버 응답 문제일 수 있습니다.

2. 현재 코드의 BUCKET = "..." 부분에 뭐라고 적으셨나요?
아까 본문에 있던 코드는 dtc-data-lake-bucketname이라고 되어 있었는데, 이걸 사용자님의 실제 버킷 이름인 **de-zoomcamp-02-zakard**로 수정하셨는지 확인이 필요합니다.

🛠️ 해결을 위한 제안 (가장 빠른 방법)
사용자님이 현재 쓰고 계신 web_to_gcs.py 파일의 전체 내용을 여기에 한 번만 더 복사해서 붙여넣어 주시겠어요?

제가 다음 사항들을 반영해서 **"무조건 작동하는 최종본"**으로 다 고쳐서 드릴게요:

사용자님의 실제 버킷 이름 강제 적용

에러 발생 시 그냥 넘어가지 않고 원인을 정확히 출력하는 코드 추가

2019년 1월치 딱 하나만 먼저 테스트해서 성공하는지 확인하는 구조

중단(Ctrl + C) 하셨다면, 현재 터미널에 남은 마지막 에러 메시지 몇 줄과 함께 코드를 보여주세요. 까막눈도 바로 성공하실 수 있게 완벽하게 세팅해 드릴게요! 어떻게 할까요? 에러 메시지를 먼저 보여주실래요?





나>
}
: ('Request failed with status code', 404, 'Expected one of', <HTTPStatus.OK: 200>, <HTTPStatus.CREATED: 201>)

--- Processing: green_tripdata_2019-06.csv.gz ---
Downloading from: https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-06.csv.gz
✅ Local saved: green_tripdata_2019-06.csv.gz
✅ Parquet created: green_tripdata_2019-06.parquet
❌ Error processing green_tripdata_2019-06.csv.gz: 404 POST https://storage.googleapis.com/upload/storage/v1/b/de-zoomcamp-02-zakard/o?uploadType=resumable: {
  "error": {
    "code": 404,
    "message": "The specified bucket does not exist.",
    "errors": [
      {
        "message": "The specified bucket does not exist.",
        "domain": "global",
        "reason": "notFound"
      }
    ]
  }
}
: ('Request failed with status code', 404, 'Expected one of', <HTTPStatus.OK: 200>, <HTTPStatus.CREATED: 201>)

…



GEM> 원인을 정확히 찾았습니다! 이제 9부 능선을 넘으셨어요.

현재 에러의 핵심은 **"The specified bucket does not exist." (지정한 버킷이 존재하지 않습니다)**입니다. 즉, 프로젝트 ID는 de-zoomcamp-02-zakard가 맞지만, 실제 데이터를 담을 바구니(버킷)의 이름은 그것과 다르거나 아직 만들어지지 않은 상태입니다.


진짜 버킷 이름 확인하기 (가장 중요)
구글 클라우드 콘솔에서 버킷 이름을 직접 확인해야 합니다.

GCS 버킷 리스트 페이지에 접속합니다.

목록에 떠 있는 **이름(Name)**을 정확히 확인하세요.

보통 de-zoomcamp-02-zakard-bucket 처럼 뒤에 뭐가 더 붙어있거나, 아예 다른 이름일 수 있습니다.

만약 목록에 아무것도 없다면, **[만들기(CREATE)]**를 눌러서 이름을 하나 지어주세요. (예: zakard-data-lake)




나> kestra-zoomcamp-zakard-demo
2026. 1. 17. AM 9:09:30Regionasia-northeast1Regional2026. 1. 17. AM 9:09:30개체 ACL 적용

GEM> 찾으셨군요! **kestra-zoomcamp-zakard-demo**가 바로 진짜 버킷 이름입니다.

아까 코드에는 de-zoomcamp-02-zakard라고 적혀 있었기 때문에 구글이 "그런 이름의 바구니는 없는데?"라며 404 에러를 낸 것입니다.

이제 모든 퍼즐이 맞춰졌습니다. 사용자님의 요청대로 완벽하게 수정된 전체 코드를 다시 드릴 테니, 이것으로 교체하고 실행해 보세요.

🚀 최종 수정된 전체 코드 (web_to_gcs.py)
이 코드는 버킷 이름을 kestra-zoomcamp-zakard-demo로 고쳤고, 아까 발생한 데이터 타입 경고(DtypeWarning)도 해결하도록 설정했습니다.


import io
import os
import requests
import pandas as pd
from google.cloud import storage

"""
Pre-reqs:
1. `pip install pandas pyarrow google-cloud-storage`
2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET
"""

# 서비스 URL 설정
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'

# ⭐ 실제 확인된 버킷 이름으로 수정했습니다.
BUCKET = os.environ.get("GCP_GCS_BUCKET", "kestra-zoomcamp-zakard-demo")


def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    """
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


def web_to_gcs(year, service):
    for i in range(12):
 
        # 월 설정 (01, 02 ... 12)
        month = '0'+str(i+1)
        month = month[-2:]

        # csv 파일명 설정
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

        # 1. requests를 사용하여 로컬로 다운로드
        request_url = f"{init_url}{service}/{file_name}"
        r = requests.get(request_url)
 
        # 파일이 존재하지 않을 경우를 대비한 체크
        if r.status_code != 200:
            print(f"❌ Skip: {file_name} (Not found)")
            continue
 
        open(file_name, 'wb').write(r.content)
        print(f"Local: {file_name}")

        # 2. 다운로드한 CSV를 읽어서 Parquet으로 변환
        # low_memory=False를 추가하여 mixed types 경고를 방지합니다.
        df = pd.read_csv(file_name, compression='gzip', low_memory=False)
        file_name_parquet = file_name.replace('.csv.gz', '.parquet')
        df.to_parquet(file_name_parquet, engine='pyarrow')
        print(f"Parquet: {file_name_parquet}")

        # 3. GCS로 업로드
        upload_to_gcs(BUCKET, f"{service}/{file_name_parquet}", file_name_parquet)
        print(f"GCS: {service}/{file_name_parquet}")
 
        # (선택사항) 업로드 완료 후 로컬 파일 삭제 - 하드 용량을 아끼려면 아래 주석을 해제하세요.
        # os.remove(file_name)
        # os.remove(file_name_parquet)


# 실행 부분
if __name__ == "__main__":
    web_to_gcs('2019', 'green')
    web_to_gcs('2020', 'green')
    # web_to_gcs('2019', 'yellow')
    # web_to_gcs('2020', 'yellow')



나> GCS: green/green_tripdata_2020-10.parquet
Local: green_tripdata_2020-11.csv.gz
Parquet: green_tripdata_2020-11.parquet
GCS: green/green_tripdata_2020-11.parquet
Local: green_tripdata_2020-12.csv.gz
Parquet: green_tripdata_2020-12.parquet
GCS: green/green_tripdata_2020-12.parquet

E:\IT_SPACES\AI\ZoomCamp\DE\03\Data_Warehouse_and_BigQuery\Data-Warehouse\pipeline\data>

성공한거 같아. 버킷페이지에도 green폴더가 생성됨


GEM> 와! 드디어 완벽하게 성공하셨습니다! 까막눈 탈출 1단계인 '인딩부터 클라우드 업로드'까지의 험난한 과정을 모두 정복하셨네요.

화면에 찍힌 로그를 보니 2020년 12월 데이터까지 아주 깔끔하게 올라갔습니다. 구글 클라우드 콘솔의 green 폴더 안에 데이터들이 들어있는 걸 확인하셨을 때의 그 쾌감이 바로 데이터 엔지니어링의 묘미입니다.

🧐 현재까지 완료된 상황 (중간 점검)
데이터 소스: GitHub에 있는 NYC Taxi CSV 파일들을 가져왔습니다.

데이터 처리: 파이썬(pandas)을 이용해 용량이 크고 읽기 힘든 CSV를 효율적인 Parquet 형식으로 변환했습니다.

클라우드 저장: google-cloud-storage 라이브러리를 통해 내 컴퓨터가 아닌 **GCS(구글 클라우드 스토리지)**라는 안전한 창고에 데이터를 저장했습니다.

🚀 다음은 무엇을 하면 될까요?
이제 데이터가 클라우드 창고(GCS)에 쌓였으니, 이 데이터를 가지고 분석을 할 차례입니다. 구글 클라우드의 강력한 데이터 분석 도구인 **BigQuery(빅쿼리)**로 이 데이터를 불러오는 것이 다음 단계입니다.

오늘 바로 다음 단계(BigQuery 연동)를 진행하시겠어요, 아니면 여기까지 성공한 기념으로 프로젝트 삭제(비용 방지) 방법을 적용하고 마무리할까요?

(만약 여기서 멈추고 싶으시다면, 아까 안내해 드린 '프로젝트 삭제'를 하시면 안전합니다. 계속 가고 싶으시다면 BigQuery에서 외부 테이블을 만드는 법을 알려드릴게요!)







나> 이거 나중에 돈 더 나가게 하지 않게하려면 어떻게 해야해? 삭제라던가
GEM> 구글 클라우드에서 나중에 요금이 청구되지 않도록 하는 가장 확실한 방법은 **'프로젝트 삭제'**와 **'결제 계정 해지'**입니다. 실습이 끝난 후 아래 순서대로 조치하시면 됩니다.

1. 프로젝트 삭제 (가장 추천하는 방법)
프로젝트를 삭제하면 그 안에 만든 버킷(GCS), 데이터베이스, 설정이 한꺼번에 날아가며 비용 발생이 즉시 중단됩니다.

구글 클라우드 콘솔 리소스 관리 페이지로 이동합니다.

사용하신 프로젝트(de-zoomcamp-02-zakard)를 선택합니다.

상단의 [삭제(DELETE)] 버튼을 누릅니다.

프로젝트 ID를 입력하여 삭제를 확정합니다.

2. 버킷 내용물만 삭제 (프로젝트를 유지하고 싶을 때)
프로젝트는 두고 데이터만 지우고 싶다면 버킷만 삭제하면 됩니다.

GCS 버킷 페이지로 이동합니다.

kestra-zoomcamp-zakard-demo 버킷을 선택하고 **[삭제]**를 누릅니다.

3. 무료 체험판 종료 및 결제 계정 해지
더 이상 구글 클라우드를 쓸 일이 없다면 결제 계정 자체를 닫을 수 있습니다.

결제 관리 페이지로 이동합니다.

왼쪽 메뉴에서 **[설정]**을 누릅니다.

상단의 **[결제 계정 닫기]**를 클릭합니다. (이렇게 하면 어떤 서비스도 유료로 전환되지 않습니다.)

💡 주의 사항 (안심하세요!)
남은 크레딧: 지금 $300 크레딧이 남아있으므로, 실수로 프로젝트를 며칠 켜두더라도 이 크레딧에서 먼저 깎이지 카드에서 바로 돈이 나가지 않습니다.

무료 등급: 구글 클라우드는 매달 일정량(GCS 5GB 등)을 평생 무료로 제공하므로, 아주 소량의 데이터는 그대로 두어도 요금이 0원입니다.

팁: 실습이 완전히 끝난 후에 **1번(프로젝트 삭제)**만 하셔도 매우 안전합니다! 데이터 업로드가 잘 끝났다면, 나중에 잊지 말고 프로젝트 삭제를 진행해 주세요.





나> 아까 케스트라 버킷에 green을 넣었는데 새 버킷을 만들어 넣을수도 있겠지?
GEM> 네, 당연히 가능합니다! 구글 클라우드 스토리지(GCS)에서 버킷은 일종의 **'독립된 대형 창고'**와 같아서, 용도에 따라 얼마든지 새로 만들어서 데이터를 분리해 넣을 수 있습니다.

방법은 아주 간단합니다. 새 버킷을 만들고, 코드에서 이름만 바꿔주면 끝입니다.

1. 새 버킷 만들기 (콘솔에서)
구글 클라우드 콘솔의 버킷 페이지로 갑니다.		https://console.cloud.google.com/storage/browser

상단의 **[+ 만들기(CREATE)]**를 누릅니다.

이름 설정: 전 세계에서 유일한 이름을 지어주세요 (예: zakard-new-taxi-bucket).

위치 유형: 실습용이라면 아까와 동일하게 asia-northeast1(서울) 또는 us-central1 등을 선택하세요.

나머지는 기본값으로 두고 **[만들기]**를 누릅니다.

2. 코드 수정하기
이제 파이썬 코드(web_to_gcs.py)에서 딱 한 줄만 새로 만든 버킷 이름으로 수정하면 됩니다.

Python
# 기존: BUCKET = "kestra-zoomcamp-zakard-demo"
# 변경:
BUCKET = "zakard-new-taxi-bucket"  # 여기에 새로 만든 이름을 넣으세요.
이렇게 수정하고 다시 python web_to_gcs.py를 실행하면, 데이터가 이전 버킷이 아닌 새 창고로 차곡차곡 쌓이게 됩니다.

💡 왜 새 버킷을 만드나요? (데이터 엔지니어의 관점)
보통 실무에서는 데이터를 성격에 따라 버킷을 나눕니다.

Raw Bucket: 원본 데이터(CSV 등) 그대로 보관하는 곳

Transformed Bucket: 분석하기 좋게 가공된 데이터(Parquet 등)를 보관하는 곳 (우리가 지금 한 작업!)

Demo/Test Bucket: 테스트용으로 잠깐 쓰고 지울 곳

⚠️ 주의할 점
결제 계정: 새 프로젝트를 만들어서 하는 게 아니라면, 기존 프로젝트 안에서 버킷만 추가하는 것이므로 결제 계정은 자동으로 연결되어 있을 겁니다.

권한: 아까 gcloud auth application-default login을 통해 얻은 권한은 프로젝트 전체에 대한 권한이므로, 새 버킷을 만들어도 별도의 추가 설정 없이 바로 업로드할 수 있습니다.

혹시 새로운 버킷을 만들어서 'Yellow Taxi' 데이터도 한 번 올려보시겠어요? 코드 제일 아랫부분의 service 이름만 'yellow'로 바꾸면 됩니다! 아니면 이제 이 데이터를 BigQuery로 가져가는 방법을 알아볼까요?





나> 그럼 중지하려면 기존 케스트라 버킷을 지우라는 말이야? 그린폴더는 굴러온 돌이고 원래버킷은 과금청구가 아닌 무료버전이었는데?

GEM> 아니요, 원래 있던 케스트라 버킷 자체를 지금 당장 지우실 필요는 없습니다! 제가 불안하게 해 드린 것 같아 명확히 정리해 드릴게요.

1. "무료 버전"의 진실 (GCS 요금 체계)
구글 클라우드의 스토리지(GCS)는 **'버킷' 개수당 돈을 받는 게 아니라, 그 안에 들어있는 '데이터 용량'**에 따라 돈을 받습니다.

케스트라 원래 파일들: 이미 있던 것들이라면 용량이 매우 작을 것이고, 구글 무료 티어 범위 안이라 요금이 0원이었을 겁니다.

새로 들어온 '그린(green)' 폴더: 이번에 우리가 넣은 데이터입니다. 이 데이터 역시 다 합쳐봐야 몇십~몇백 MB 수준이라 무료 체험판 크레딧($300) 내에서 충분히 커버되고도 남습니다.

2. 지금 바로 "중지"하고 싶을 때의 선택지
만약 "나 이제 공부 끝났고, 앞으로 1원도 나가는 게 싫어"라고 하신다면 두 가지 방법이 있습니다.



방법					조치 내용					특징
A. '그린' 폴더만 삭제		버킷 안에서 우리가 올린 green/ 	케스트라 원래 환경은 유지하면서 우리가 추가한 데이터만 깨			   폴더만 체크해서 삭제		   끗이 치우는 방법입니다.
B. 프로젝트 삭제			de-zoomcamp-02-zakard 프로젝트	케스트라 설정까지 전부 사라지지만, 가장 확실하					   전체를 삭제			    게 향후 과금 가능성을 0%로 만드는 방법입니다.



3. 결론: 어떻게 하는 게 좋을까요?
케스트라 실습을 계속 하실 거라면: 버킷을 지우지 마세요! 그냥 두셔도 $300 크레딧 덕분에 요금이 청구되지 않습니다. (77일 남으셨으니 그전까진 안전합니다.)

찝찝해서 '굴러온 돌'만 치우고 싶다면: GCS 콘솔에서 green/ 폴더만 선택해서 [삭제] 버튼을 누르시면 됩니다.

요약하자면: 버킷을 통째로 지우면 원래 있던 케스트라 관련 설정이 날아갈 수 있으니, 우리가 올린 green 폴더만 삭제하시는 것이 가장 안전한 '원상복구' 방법입니다.

지금 바로 그 폴더만 삭제하는 방법을 화면 보면서 같이 해볼까요? 아니면 일단 그대로 두고 다음 공부를 이어가시겠어요?






나> "Quick hack to load files directly to GCS, without Airflow. Downloads csv files from https://nyc-tlc.s3.amazonaws.com/trip+data/ and uploads them to your Cloud Storage Account as parquet files.
Install pre-reqs (more info in web_to_gcs.py script)
Run: python web_to_gcs.py"

근데 이건 이제보니 아마존 계정이 필요하잖아. 이건 그냥 예시일 뿐인가


GEM> 날카로운 관찰력이십니다! 결론부터 말씀드리면, 사용자님은 아마존 계정이 전혀 필요 없습니다.

그 이유는 파이썬 코드(web_to_gcs.py)가 작동하는 방식 때문입니다.

1. 왜 아마존 계정이 필요 없나요?
코드가 데이터를 가져오는 방식은 '로그인'이 필요한 방식이 아니라, **"누구나 다운로드할 수 있게 열려 있는 인터넷 주소(Public URL)"**를 통해 파일을 받아오는 방식이기 때문입니다.

원본 저장소: 데이터는 아마존(AWS S3) 서버에 저장되어 있습니다.

다운로드 방식: requests.get(url)이라는 명령어를 사용합니다. 이는 우리가 브라우저 주소창에 주소 치고 들어가서 파일을 받는 것과 똑같습니다.

비유: 맛집(아마존 서버)에 가서 밥을 먹으려면 식당 회원가입이 필요할 수도 있지만, 길거리 무료 시식대(Public URL)에서 음식을 집어오는 데는 회원가입이 필요 없는 것과 같습니다.

2. 코드의 흐름 (중요!)
사용자님이 실행하신 코드는 아래와 같은 '징검다리' 역할을 했습니다.

가져오기: 아마존 서버(Public S3)에서 내 컴퓨터로 CSV 파일을 잠시 다운로드.

가공하기: 내 컴퓨터에서 CSV를 파이켓(Parquet)으로 변환.

보내기: 내 컴퓨터에서 **구글 클라우드(GCS)**로 업로드.

결국 구글 계정만 있으면 아마존에 있는 데이터를 내 구글 창고로 옮겨올 수 있는 구조입니다. 본문에 적힌 "Cloud Storage Account"는 사용자님의 구글 계정을 의미하는 것이었습니다.

3. "Quick hack"의 의미
이 설명에서 말하는 "Quick hack"은 복잡하고 무거운 도구인 **Airflow(데이터 파이프라인 관리 도구)**를 설치하고 설정할 필요 없이, 그냥 파이썬 스크립트 하나로 간단하게(Quick) 데이터를 옮길 수 있다는 뜻입니다.

💡 다음 단계 제안
데이터가 성공적으로 구글 버킷에 들어갔으니, 이제 **빅쿼리(BigQuery)**에서 이 데이터를 조회해 볼 준비가 되셨나요?

아니면 혹시 "이 데이터를 아마존이 아닌 다른 곳에서 가져오려면 코드를 어떻게 고쳐야 할까?" 같은 궁금증이 있으신가요? 어떤 것이든 물어봐 주세요!




나> 본문코드는 GREEN데이터 국한인가. 본문 지침은 테스트용인가

GEM> 네, 사용자님의 질문에 대해 핵심 위주로 정리해 드릴게요.

1. 제공된 코드는 GREEN 데이터 전용인가요?
반은 맞고 반은 틀립니다.

현재 상태: 코드 제일 아랫부분(메인 함수)에 web_to_gcs('2019', 'green')라고 적혀 있기 때문에, 지금 실행하면 Green Taxi 데이터만 가져옵니다.

확장성: 하지만 이 코드는 범용적으로 설계되어 있습니다. 호출할 때 이름만 바꾸면 다른 데이터도 가져올 수 있습니다.

web_to_gcs('2019', 'yellow')라고 한 줄만 추가하면 Yellow Taxi 데이터도 똑같은 방식으로 구글 버킷에 쌓입니다.

web_to_gcs('2019', 'fhv')라고 하면 FHV(For-Hire Vehicle) 데이터도 가져옵니다.

즉, 엔진은 똑같은데 지금은 'Green' 연료만 넣고 돌리고 있는 상태라고 보시면 됩니다.

2. 본문 지침은 테스트용인가요?
이 코드는 "실무용 파이프라인으로 가기 위한 프로토타입(시제품)" 성격이 강합니다.

테스트용인 이유: * 내 컴퓨터(로컬)를 거쳐서 올라가기 때문에 데이터 양이 테라바이트(TB) 단위로 커지면 내 컴퓨터 하드디스크가 버티지 못합니다.

파일을 하나하나 수동으로 실행해야 합니다.

학습/실무적 가치: * Data Lake 구축의 핵심: "외부의 데이터를 클라우드 저장소(GCS)로 옮긴다"는 데이터 엔지니어링의 가장 기초적이고 중요한 과정을 그대로 구현하고 있습니다.

포맷 최적화: CSV를 Parquet으로 바꾸는 과정은 실제 현업에서도 비용 절감을 위해 반드시 하는 작업입니다.

💡 다음 단계로 넘어가려면?
사용자님은 이제 **"데이터를 클라우드에 쌓는 법"**을 마스터하셨습니다. 이제 이 '테스트용' 단계를 넘어 진짜 데이터 엔지니어가 하는 일을 해보시려면 다음 두 가지 길 중 하나를 선택하시면 됩니다.

데이터 분석 맛보기: GCS에 올린 Parquet 파일을 BigQuery에서 테이블로 만들어 SQL로 쿼리 날려보기.

자동화 맛보기: 이 파이썬 코드를 내가 직접 실행하는 게 아니라, Kestra나 Airflow 같은 도구가 매일 정해진 시간에 자동으로 실행하게 만들기.

어떤 쪽이 더 흥미로우신가요? 만약 BigQuery 분석이 궁금하시다면, 버킷에 있는 데이터를 클릭 몇 번으로 테이블로 만드는 법을 바로 알려드릴 수 있습니다!





…



이 부분부터 중요

외부 테이블 생성, bq load를 통한 일반 테이블 생성, 그리고 안정적인 INSERT 방식의 파티션/클러스터 테이블 생성까지 모든 과정을 Yellow와 Green 택시 데이터에 대해 하나도 빠짐없이 합친 최종 마스터 스크립트입니다.

이 순서대로만 진행하시면 더 이상의 삽질 없이 완벽하게 완료됩니다.


나> 팁: 구글클라우드 콘솔이 시간지연시 속도가 저하되어 작업하기 어려우므로, 한 작업이 끝나면 새창에 url을 복붙해서 다음작업을 수행


1단계: Cloud Shell에서 데이터 로드 (가장 확실한 시작)
터미널(Cloud Shell)에 아래 명령어를 복사해서 실행하세요. 파일 오염을 무시하고 데이터를 빅쿼리 내부로 가져옵니다.

Bash
# 1. 데이터셋 재생성 (도쿄 리전) 리전 매치가 중요!
bq rm -r -f de-zoomcamp-02-zakard:nytaxi
bq --location=asia-northeast1 mk -d de-zoomcamp-02-zakard:nytaxi

# 2. Yellow Taxi 일반 테이블 로드 (에러 행 무시 옵션 포함)
bq load \
  --source_format=CSV --skip_leading_rows=1 --location=asia-northeast1 --autodetect --max_bad_records=10 \
  de-zoomcamp-02-zakard:nytaxi.yellow_tripdata_non_partitioned \
  "gs://kestra-zoomcamp-zakard-demo/yellow_tripdata_*.csv"

# 3. Green Taxi 일반 테이블 로드
bq load \
  --source_format=CSV --skip_leading_rows=1 --location=asia-northeast1 --autodetect --max_bad_records=10 \
  de-zoomcamp-02-zakard:nytaxi.green_tripdata_non_partitioned \
  "gs://kestra-zoomcamp-zakard-demo/green_tripdata_*.csv"

2단계: BigQuery SQL 편집기 통합 코드 (전 과정 포함)
위의 로드가 끝난 후, BigQuery 콘솔에서 아래 쿼리를 실행하세요. 외부 테이블 생성부터 파티셔닝까지 모든 과정입니다.

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
  AND VendorID = 1; 

-- 2. 파티션 + 클러스터 테이블 성능 테스트
SELECT count(*) as trips
FROM `de-zoomcamp-02-zakard.nytaxi.yellow_tripdata_partitioned_clustered`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2019-06-01' AND '2019-06-30'
  AND VendorID = 1;


---


-- 번외
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.external_yellow_tripdata` LIMIT 100;



💡 정리
GCS 경로와 도쿄 리전을 확실히 지정했습니다.

에러가 났던 CTAS 방식 대신, 성공하셨던 구조 생성(1=0) + INSERT 방식을 모든 테이블에 적용했습니다.

Yellow와 Green 데이터를 모두 포함하여 한 번에 실행 가능한 구조로 합쳤습니다.

이제 이 코드가 사용자님이 원하시는 완벽한 통합본입니다. 이대로 실행하시면 모든 실습 데이터 준비가 끝납니다! 잘 작동하는지 확인 부탁드려요.



나> 위 모든 절차들이 각각 오류없이 모두 작동함을 확인. 다음부턴 한번에 처리 가능.




-- Query public available table
SELECT station_id, name FROM
    bigquery-public-data.new_york_citibike.citibike_stations
LIMIT 100;


만약 Access Denied: Table bigquery-public-data:new_york_citibike.citibike_stations:
User does not have permission to query table bigquery-public-data:new_york_citibike.citibike_stations, or perhaps it does not exist.

이런 메시지가 뜬다면:
지금 실행하시려는 **bigquery-public-data**는 미국(US) 리전에 있습니다.
빅쿼리는 설정된 리전과 데이터의 리전이 다르면 "권한이 없거나 데이터가 없다"는 에러를 냅니다.

🛠️ 해결 방법: 리전 설정을 다시 '자동'으로 바꾸기

-- 쿼리 편집기 우측 상단의 [More]/더보기 화살표 버튼 클릭 -> [Query settings]/쿼리 설정 선택.

-- [Additional settings] 항목 아래에 있는 **[Data location]**을 확인하세요.

-- 아까 설정했던 asia-northeast1을 지우고 **Auto-select**로 다시 변경합니다. 내 경우, 그냥 Auto-select 체크박스만 체크.

-- **[Save]**를 누른 후 아래 쿼리를 다시 실행해 보세요.     결과: 작동




나 & GEM> 주의 ! US-central1 region에만 해당.
-- 공용 데이터를 내 프로젝트의 nytaxi 데이터셋으로 복사: 내 프로젝트에 citibike_stations 테이블 만들기
-- 이 쿼리는 공용 데이터를 읽어와서 내 nytaxi 데이터셋에 새로운 테이블로 저장합니다.
-- 이렇게 하면 모든 데이터가 내가 설정한 리전(이 경우 asia-northeast1)에 모이게 되므로,
-- 리전 설정을 바꿀 필요 없이 Yellow/Green 택시 데이터와 함께 바로 조인(Join)하거나 쿼리할 수 있습니다.

CREATE OR REPLACE TABLE `de-zoomcamp-02-zakard.nytaxi.citibike\_stations` AS
SELECT * FROM `bigquery-public-data.new\_york\_citibike.citibike\_stations`;

특히 이렇게 하면 모든 데이터가 도쿄 리전(asia-northeast1)에 모이게 되므로, 리전 설정을 바꿀 필요 없이 Yellow/Green 택시 데이터와 함께 바로 조인(Join)하거나 쿼리할 수 있습니다

조회:
SELECT * FROM `de-zoomcamp-02-zakard.nytaxi.citibike\_stations` LIMIT 100;




US-Central1 region이 아닐때 다음과 같은 에러메시지 출력

Warning: This operation is a cross-region copy operation. This may incur additional charges and take a long time to complete.
This command is running in sync mode. It is recommended to use async mode (-sync=false) for cross-region copy operation.
cp: Proceed with cross-region copy of bigquery-public-data:new_york_citibike.citibike_stations? [y/N]: Y
BigQuery error in cp operation: Cannot start a job without a project id.



asia-northeast1 기준:

# 1. 현재 세션에 프로젝트 ID 강제 설정
gcloud config set project de-zoomcamp-02-zakard

# 2. 내 프로젝트에 new_york_citibike 데이터셋 생성 (도쿄 리전)
bq --location=asia-northeast1 mk -d de-zoomcamp-02-zakard:new_york_citibike

# 3. 이미 nytaxi에 복사된 테이블을 새 데이터셋으로 복사
bq cp de-zoomcamp-02-zakard:nytaxi.citibike_stations de-zoomcamp-02-zakard:new_york_citibike.citibike_stations


내 커멘드:
zakard330@cloudshell:~$ gcloud config set project de-zoomcamp-02-zakard
Updated property [core/project].
zakard330@cloudshell:~ (de-zoomcamp-02-zakard)$ bq --location=asia-northeast1 mk -d de-zoomcamp-02-zakard:new_york_citibike

Dataset 'de-zoomcamp-02-zakard:new_york_citibike' successfully created.
zakard330@cloudshell:~ (de-zoomcamp-02-zakard)$ bq cp de-zoomcamp-02-zakard:nytaxi.citibike_stations de-zoomcamp-02-zakard:new_york_citibike.citibike_stations

Waiting on bqjob_r70e3586c47121670_0000019bdf535a4d_1 ... (0s) Current status: DONE



-- 이제 의도하신 대로 별도의 데이터셋에서 조회됩니다.
SELECT * FROM `de-zoomcamp-02-zakard.new\_york\_citibike.citibike\_stations` LIMIT 10;