# Agent Relay — local homework image (SQLite starter)
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install uv, then project deps from lockfile (no dev group)
COPY --from=ghcr.io/astral-sh/uv:0.9.13 /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev \
    && mkdir -p /app/data

ENV PATH="/app/.venv/bin:$PATH"
ENV RELAY_DATABASE_URL="sqlite:////app/data/agent-relay.db"

EXPOSE 8000

# Must bind 0.0.0.0 so host `-p` publishing works (127.0.0.1 would look broken).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
