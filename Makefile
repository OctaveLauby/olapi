.PHONY: help check format int sync typecheck rebuild run

help:
	@echo "sync ................ update venv"
	@echo "format .............. run ruff formatter"
	@echo "lint ................ run ruff lint check"
	@echo "typecheck ........... run pyright type checker"
	@echo "check ............... run lint and typecheck"
	@echo "rebuild ............. remove containers, api image, volumes and rebuild"
	@echo "run ................. start all services"

sync:
	uv sync

format:
	poetry run ruff check --fix .                                                                                                                                                                                        
	poetry run ruff format .

lint:
	poetry run ruff check src
	poetry run ruff format --check

typecheck:
	uv run pyright src

check: lint typecheck

rebuild:
	docker compose down --rmi local -v
	docker compose build

run:
	docker compose up
