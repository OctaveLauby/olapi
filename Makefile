.PHONY: help check format int sync typecheck rebuild run test ci

help:
	@echo "Options (local run):"
	@echo "run ................. start all services"
	@echo "rebuild ............. remove and rebuild all containers, api image, all volumes"
	@echo ""
	@echo "Options (contribute):"
	@echo "sync ................ update venv"
	@echo "format .............. run ruff formatter"
	@echo "lint ................ run ruff lint check"
	@echo "typecheck ........... run pyright type checker"
	@echo "check ............... run lint and typecheck"
	@echo "test ................ run the test suite"
	@echo "ci .................. run sync, lint, check and test"

# Setup

sync:
	uv sync

rebuild:
	docker compose down --rmi local -v
	docker compose build

run:
	docker compose up


# Contribute

format:
	poetry run ruff check --fix .                                                                                                                                                                                        
	poetry run ruff format .

lint:
	poetry run ruff check src
	poetry run ruff format --check

typecheck:
	uv run pyright


check: lint typecheck


test:
	uv run pytest

ci: sync lint check test
