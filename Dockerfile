FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY libs ./libs
COPY apps ./apps

RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

# The olapi app is a flat uv-app; run it from its own directory so `main:app` resolves.
WORKDIR /app/apps/olapi

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
