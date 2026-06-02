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
- ADD migrations
- ADD Rate Limiter
- ADD Settings management (dotenv or config files)
- REWORK Authentication
    - Activate Keycloak secret
    - Remove auth endpoints and let keycloak handle the authentication (e.g. `standardFlowEnabled=true & directAccessGrantsEnabled=false` in realm.json)
