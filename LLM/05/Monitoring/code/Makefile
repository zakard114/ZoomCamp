# ==============================================================================
# Course Assistant Project - Makefile
# ==============================================================================

make run:
	# Run the RAG pipeline (assistant.py) locally with uv.
	uv run python assistant.py

chat:
	# Launch the Streamlit chat UI (app.py).
	uv run streamlit run app.py

dashboard:
	# Run the Streamlit metrics dashboard in headless mode.
	uv run streamlit run dashboard.py --server.headless true

build:
	# Build or rebuild images defined in docker-compose.yaml.
	docker compose build

up:
	# Start all Compose services in the background.
	docker compose up -d

down:
	# Stop and remove Compose containers/networks.
	docker compose down

logs:
	# Follow Compose service logs.
	docker compose logs -f

# Shortcut: rebuild images then start the stack.
stack: build up

init-db:
	# Create initial PostgreSQL schema via db_init.py.
	uv run python db_init.py

network:
	# Create the 'monitoring' Docker network for container communication.
	docker network create monitoring

# Starts PostgreSQL after ensuring the monitoring network exists.
postgres: network
	# Run Postgres 17 on the monitoring network with local port 5432 and pgdata volume.
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
	# Smoke-test DB connection and list current records via db_query.py.
	uv run python db_query.py
