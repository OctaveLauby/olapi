# Python API Template

This repository aims to provide a proper template to build your API upon.

## Setup

Requirements:

- uv (tested with v0.8.3)
- docker (tested with v29.3.1)

**Start stack**:

```bash
make run
```

```bash
# Rebuild your containers (clean data)
make rebuild
```

Then:

* **Requests on API**: `uv run --directory apps/olapi python -m scripts.request_api`
* **See swagger**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Check keycloak users**: [http://localhost:8080/admin/master/console/#/olapi/users](http://localhost:8080/admin/master/console/#/olapi/users)
    * username=admin
    * password=admin
* **Check database content**, using your favourite database viewer:
    * host name / address: localhost
    * port: 5430
    * username: olapai
    * password: olapai


## Implementation

### Stack

- **uv** for dependency management, with main libraries:
    - **sqlalchemy**
    - **ruff**
    - **pyright**
    - **pytest**
- **fastapi** for api implementation
- **pydantic** for data validation
- **postgres** as database
- **Keycloak** for production ready authentication:
    - Authentication done through **Keycloak**
    - Will keep the `POST /login` and `POST /users` endpoints, but ideally it is done through FE redirections to Keycloak.
    - Token validation in the API
    - Not storing password in my db


### Structure

Using [uv workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/):

```
  .
  ├── Makefile
  ├── README.md
  ├── CONTRIBUTING.md
  ├── docker-compose.yml
  ├── pyproject.toml
  ├── ...
  ├── docker/                    # docker stack config
  │   ├── Dockerfile             # api image build
  │   └── keycloak/              # keycloak realm import
  │       └── ...
  ├── apps/
  │   └── olapi/                 # FastAPI application (flat uv-app)
  │       ├── main.py
  │       ├── settings.py
  │       ├── ...
  │       ├── models/            # tables
  │       ├── routers/           # endpoints
  │       ├── dtos/              # dtos
  │       ├── scripts/           # API usage scripts
  │       ├── tests/
  │       └── pyproject.toml
  └── libs/
      └── authentication/        # Keycloak client (packaged library)
          ├── src/authentication/
          │   └── ...
          ├── tests/
          └── pyproject.toml
```

### Shortcuts

* **No store layer** to isolate database operations
* **No service layer** to isolate business logic
* **No entities vs dtos distinction** to isolate interfaces from processes (would require store/service layer) 
