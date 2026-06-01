.PHONY: install dev test lint format docker-up docker-down seed eval clean help streamlit

install:
	/Users/ashutoshkumar/.local/bin/uv sync --project backend --extra dev

dev:
	PYTHONPATH=. /Users/ashutoshkumar/.local/bin/uv run --project backend uvicorn src.main:create_app --factory --reload --host 0.0.0.0 --port 8000

test:
	PYTHONPATH=. /Users/ashutoshkumar/.local/bin/uv run --project backend --extra dev pytest

lint:
	PYTHONPATH=. /Users/ashutoshkumar/.local/bin/uv run --project backend ruff check src tests && PYTHONPATH=. /Users/ashutoshkumar/.local/bin/uv run --project backend mypy src

format:
	PYTHONPATH=. /Users/ashutoshkumar/.local/bin/uv run --project backend ruff format src tests && PYTHONPATH=. /Users/ashutoshkumar/.local/bin/uv run --project backend black src tests

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down -v

seed:
	PYTHONPATH=. /Users/ashutoshkumar/.local/bin/uv run --project backend python -m backend.src.shared.seed

eval:
	PYTHONPATH=. /Users/ashutoshkumar/.local/bin/uv run --project backend python -m backend.src.evaluation.eval_runner

streamlit:
	PYTHONPATH=. /Users/ashutoshkumar/.local/bin/uv run --project backend streamlit run streamlit_app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

help:
	@echo "NomadIQ Makefile Command Reference:"
	@echo "  install      Install backend dev dependencies"
	@echo "  dev          Run local backend FastAPI server with hot-reload"
	@echo "  test         Execute backend pytest suite"
	@echo "  lint         Run ruff and mypy static code checks"
	@echo "  format       Auto-format python code using ruff and black"
	@echo "  docker-up    Build and boot up stack via Docker Compose"
	@echo "  docker-down  Stop and destroy Docker Compose containers & volumes"
	@echo "  seed         Seed the pgvector and relational databases"
	@echo "  eval         Execute the LLM automated evaluation runner"
