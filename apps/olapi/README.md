# olapi

The Social Media API application (FastAPI).

This is a flat [uv-app](https://docs.astral.sh/uv/concepts/projects/init/#applications):
modules live directly under this directory and are imported relative to it (e.g.
`from main import app`). The app is not packaged or installed.

## Run

From the repository root:

```bash
make run        # docker compose up (postgres + keycloak + api)
```

Or directly with uvicorn from this directory:

```bash
uv run uvicorn main:app --reload
```

## Test

```bash
uv run --directory apps/olapi pytest
```
