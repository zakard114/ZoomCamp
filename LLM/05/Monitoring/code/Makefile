# ==============================================================================
# [Course Assistant Project - Automation Commands Collection (Makefile)]
# ==============================================================================

make run:
	# [ENG] Run the core RAG pipeline application locally using uv package manager.
	# [KOR] uv 패키지 매니저를 사용하여 로컬 환경에서 assistant.py(RAG 핵심 로직)를 직접 실행합니다.
	uv run python assistant.py

chat:
	# [ENG] Launch the Streamlit-based user chat interface app in the local environment.
	# [KOR] uv 패키지 매니저를 사용하여 Streamlit 기반의 유저 채팅 웹 화면(app.py)을 로컬에 구동합니다.
	uv run streamlit run app.py

dashboard:
	# [ENG] Run the Streamlit metrics dashboard in headless mode for server monitoring.
	# [KOR] uv 패키지 매니저를 사용하여 Streamlit 기반의 모니터링 대시보드(dashboard.py)를 브라우저 팝업 없이(headless) 서버 모드로 구동합니다.
	uv run streamlit run dashboard.py --server.headless true

build:
	# [ENG] Build or rebuild docker images defined in the docker-compose.yaml file.
	# [KOR] docker-compose.yaml 파일에 정의된 서비스들의 도커 이미지들을 처음부터 새로 빌드(생성)합니다.
	docker compose build

up:
	# [ENG] Start all containers managed by Docker Compose in detached background mode.
	# [KOR] 도커 컴포즈에 묶인 모든 컨테이너(앱, DB, 그라파나 등)를 백그라운드 데몬(-d) 모드로 안전하게 실행합니다.
	docker compose up -d

down:
	# [ENG] Stop and remove all running containers, networks, and volumes managed by Compose.
	# [KOR] 현재 구동 중인 도커 컴포즈 컨테이너들을 전부 안전하게 종료하고 시스템을 완전히 내립니다.
	docker compose down

logs:
	# [ENG] Fetch and follow the live system logs from all Docker Compose containers in real-time.
	# [KOR] 도커 컴포즈 컨테이너 내부에서 출력되는 시스템 로그들을 터미널 화면에 실시간으로 추적하며(-f) 계속 보여줍니다.
	docker compose logs -f

# [ENG] Sequential shortcut to trigger a full environment rebuild and immediately spin it up.
# [KOR] stack 명령어를 입력하면 자동으로 위의 'build' 단계를 먼저 거친 후 바로 'up' 단계까지 연달아 원스톱으로 실행합니다.
stack: build up

init-db:
	# [ENG] Initialize the PostgreSQL database schema and create required tables using db_init.py.
	# [KOR] uv 패키지 매니저를 사용하여 PostgreSQL 데이터베이스에 초기 테이블 스키마를 생성하는 스크립트(db_init.py)를 실행합니다.
	uv run python db_init.py

network:
	# [ENG] Create a dedicated docker bridge network named 'monitoring' for container communication.
	# [KOR] 도커 컨테이너들끼리 서로 가상 주소로 안전하게 통신할 수 있도록 'monitoring'이라는 이름의 전용 도커 네트워크망을 개설합니다.
	docker network create monitoring

# [ENG] Run a standalone PostgreSQL 17 container inside the 'monitoring' network with local volume mapping.
# [KOR] postgres 명령어가 실행되기 전에 위의 'network'망 개설 단계를 선행 조건으로 자동 실행합니다.
postgres: network
	# PostgreSQL 버전 17 엔진을 기반으로, 지정된 가상 네트워크망 안에서 로컬 5432 포트와 볼륨 데이터 볼륨(pgdata)을 매핑하여 데이터베이스 컨테이너를 수동 기동합니다.
	docker run -it \
		--name course-assistant-pg \
		--network monitoring \
		-e POSTGRES_USER=user \
		-e POSTGRES_PASSWORD=password \
		-e POSTGRES_DB=course_assistant \
		-p 5432:5432 \
		-v pgdata:/var/lib/postgresql/data \
		postgres:17

query:
	# [ENG] Execute db_query.py to test the connection and verify current records in the database.
	# [KOR] uv 패키지 매니저를 사용하여 데이터베이스에 현재 데이터가 잘 쌓이고 있는지 쿼리를 날려 검증하는 테스트 스크립트(db_query.py)를 실행합니다.
	uv run python db_query.py