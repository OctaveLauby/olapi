.PHONY: help check format int sync typecheck

help:
	@echo "sync ................ update venv"
	@echo "format .............. run ruff formatter"
	@echo "lint ................ run ruff lint check"
	@echo "typecheck ........... run pyright type checker"
	@echo "check ............... run lint and typecheck"

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
