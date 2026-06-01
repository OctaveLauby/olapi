FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src

RUN uv pip install --system -e .

EXPOSE 8000
CMD ["uvicorn", "olapi.main:app", "--host", "0.0.0.0"]
