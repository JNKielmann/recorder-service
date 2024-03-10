install:
	poetry install
test:
	poetry run pytest
format:
	poetry run ruff format
lint:
	poetry run ruff check --fix
	poetry run pyright
run:
	poetry run uvicorn recorder_service:app