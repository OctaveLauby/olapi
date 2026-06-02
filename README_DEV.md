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

Run validation (linting and typing):

```bash
make check
```

Run test:

```bash
# not implemented
```

Rebuild docker containers:

```bash
make rebuild
```


## Todo

- ADD tests
    - Keycloak client
    - API Auth protection
    - Endpoints
- ADD migrations
- ADD Rate Limiter
- ADD Settings management (dotenv or config files)
- REWORK Authentication
    - Activate Keycloak secret
    - Remove auth endpoints and let keycloak handle the authentication (e.g. `standardFlowEnabled=true & directAccessGrantsEnabled=false` in realm.json)
