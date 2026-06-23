
make run:
	uv run python assistant.py

chat:
	uv run streamlit run app.py

dashboard:
	uv run streamlit run dashboard.py --server.headless true

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

stack: build up

init-db:
	uv run python db_init.py

network:
	docker network create monitoring

postgres: network
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
	uv run python db_query.py

agent-run:
	uv run python ../HW_05/agent_main.py

agent-schema:
	docker exec -i postgres psql -U user -d course_assistant < ../HW_05/schema.sql
