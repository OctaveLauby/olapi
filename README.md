# Python API Template

This repository aims to provide a proper template to build your API upon.

## Setup

Requirements:

- uv (tested with v0.8.3)
- docker (tested with v29.3.1)

1. **Start local stack**:

    ```bash
    make run
    ```

2. **Requests on API**:

    ```bash
    uv run scripts/request_api.py
    ```

3. **Check keycloak users**: [http://localhost:8080/admin/master/console/#/olapi/users]()


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

```
  .
  ├── Makefile
  ├── README.md
  ├── README_DEV.md
  ├── docker-compose.yml
  ├── pyproject.toml
  ├── ...
  ├── keycloak/  # Settings for keycloak server
  │   └── ...
  ├── scripts/
  │   └── ...
  └── src/
      ├── authentication/        # Keycloak client
      │   └── ...
      └── olapi/                 # FastAPI application
          ├── __init__.py
          ├── main.py
          ├── settings.py
          ├── ...
          ├── models/            # tables
          │   ├── ...
          ├── routers/           # endpoints
          │   └── ...
          └── schemas/           # dtos
              └── ...
```

### Shortcuts

* **No store layer** to isolate database operations
* **No service layer** to isolate business logic
* **No entities vs dtos distinction** to isolate interfaces from processes (would require store/service layer) 
