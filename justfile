default:
    @just --list

# Start development server with hot-reload
dev-server:
    @uv run uvicorn main:app --app-dir ./mockai --port 8100 --reload

test:
    @uv run pytest --cov ./src --cov-report term:skip-covered --cov-fail-under=100  --record-mode=none --block-network

format:
    @uv run ruff check --fix
    @uv run ruff format
    @just --fmt --unstable

lint:
    @uv run ruff check
    @uv run ruff format --check
    @uv run mypy --strict
    @uv run pyright

pytest-record:
    @uv run pytest --record-mode=once
    @git ls-files --others --exclude-standard | grep 'cassettes/.*\.yaml' | xargs -r git add

run-server:
    @uv run ./src/unofficial_mapy_com_mcp/server.py

docker-build VERSION="latest":
    @docker build --no-cache -t 07pepa/unofficial_mapy_mcp:{{ VERSION }} .

docker-run:
    @docker run -d -p 8000:8000  --env-file .env 07pepa/unofficial_mapy_mcp:latest
