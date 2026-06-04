# How to Contribute

## Setup

Install interpreter:

```bash
make sync
```


## Makefile

To see all available make commands:

```bash
make help
```

Run validation (linting, typing and tests):

```bash
make ci
```


## Todo

- ADD tests
    - Keycloak client (could use `testcontainers[keycloak]` in integration tests)
    - API Auth protection
    - Endpoints
    - ADD Coverage
    - ADD html report
- ADD protection on user register (right now any one can create any number of users)
- ADD migrations (app start should not build )
- ADD Rate Limiter
- ADD ACL (RBAC or something else)
- ADD Observability (OpenTelemetry - Jaeger)
- ADD Settings management (dotenv or config files)
- ADD Proper Error management (API Problem)
- UPDATE code structure and use [uv workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/) with [app vs package vs lib conventions](https://docs.astral.sh/uv/concepts/projects/init/).

    ```
    .
    ├── ...
    ├── .venv/...
    ├── pyproject.toml
    ├── uv.lock
    ├── apps
    │   └── olapi/
    │       ├── ...
    │       ├── main.py
    │       ├── tests/...
    │       ├── pyproject.toml
    │       └── README.md
    └── libraries
        ├── ...
        └── authentication/
            ├── src/authentication/...
            ├── tests/...
            ├── pyproject.toml
            └── README.md
    ```

- REWORK Authentication
    - Activate Keycloak secret
    - Remove auth endpoints and let keycloak handle the authentication (e.g. `standardFlowEnabled=true & directAccessGrantsEnabled=false` in realm.json)
