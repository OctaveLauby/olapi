# API Template

This repository aims to provide a proper template to build your API upon.

Initial Assignement: https://github.com/SecondBrain-io/tech-interview/blob/master/developers/backend/social_media.md

## Implementation

### Design

Stack:

- **uv** for dependency management, with main libraries:
    - **sqlalchemy**
    - **ruff**
    - **mypy**
    - **pytest**
- **fastapi** (instead of flask)
- **pydantic** for endpoints validation
- **postgres** as database
- **Keycloak** for production ready authentication:
    - Authentication done through **Keycloak**
    - Will keep the `POST /login` and `POST /users` endpoints, but ideally it is done through FE redirection to Keycloak.
    - Token validation in the API
    - Not storing password in my db

Code structure:

```
  ├── docker-compose.yml          # postgres + keycloak (one-command setup)
  ├── pyproject.toml
  ├── src/olapi/
  │   ├── main.py
  │   ├── config.py               # Hardcoded settings for now
  │   ├── db.py                   # SQLAlchemy engine + session factory
  │   ├── deps.py                 # FastAPI dependencies (db session, current_user)
  │   ├── auth/
  │   │   ├── keycloak.py         # Keycloak admin + token endpoint client
  │   │   └── jwt.py              # JWT decode + JWKS validation
  │   ├── models/                 # SQLAlchemy ORM
  │   │   ├── user.py
  │   │   ├── post.py
  │   │   └── follow.py
  │   ├── schemas/                # Pydantic request/response DTOs
  │   │   ├── user.py
  │   │   ├── post.py
  │   │   └── auth.py
  │   └── routers/
  │       ├── auth.py             # POST /login ; POST /users
  │       ├── user.py
  │       └── post.py
  ├── migrations/                 # alembic
  └── tests/
      ├── conftest.py             # fixtures: test db, test client, mocked Keycloak
      ├── test_auth.py
      ├── test_user.py
      └── test_post.py

note: skipping store and service layers for simplicity.
```


### First Increment

First increment is about initiating the API with the authentication:

- ADD a postgres database
- ADD User table:
    - id
    - keycloak_id (indexed)
    - username (unicity)
    - email (unicity)
    - registration date
- ADD JWT authentication, using `keycloak`:
    - Authentication done through keycloak
    - API endpoints are protected with a check on the token
    - Token contains Keycloak user id:
        - Can get user informations using db
        - User synchronization between keycloak and db done through `POST /users`
- ADD `GET /hello` endpoint (in a temporary router), that returns a json `{"message": "Hello <username> !"}`
- ADD docker-compose file 3 containers:
    - API
    - postgres
    - Keycloak (with UI)
- NO pytest
- NO ruff / mypy

About `POST /users`:

1. Check email / username do not exist
2. Register to Keycloak
3. Save to DB
4. If 3. fails, remove from Keycloak

About `POST /login`:

1. Call Keycloak with email password, and get Keycloak_id and token
2. If Keycloak_id is not in database, add an entry (for username, generate a random name with ulid)
3. Return token


### Second Increment

- ADD ruff and mypy
- ADD tests
    - authentication flow
    - hello word (authenticated and un-authenticated)

### Third Increment

> Social Media stuff


### Evolutions

- Rate limiter
- Settings management (dotenv or config files)
- Activate Keycloak secret
- Remove auth endpoints and let keycloak handle the authentication (e.g. `standardFlowEnabled=true & directAccessGrantsEnabled=false` in realm.json)
