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
- **fastapi** for api implementation
- **pydantic** for data validation
- **postgres** as database
- **Keycloak** for production ready authentication:
    - Authentication done through **Keycloak**
    - Will keep the `POST /login` and `POST /users` endpoints, but ideally it is done through FE redirections to Keycloak.
    - Token validation in the API
    - Not storing password in my db

### Todo

- ADD setup commands
- ADD tests
- ADD migrations
- ADD Social Media Tables & Logic
- ADD Rate Limiter
- ADD Settings management (dotenv or config files)
- REWORK Authentication
    - Activate Keycloak secret
    - Remove auth endpoints and let keycloak handle the authentication (e.g. `standardFlowEnabled=true & directAccessGrantsEnabled=false` in realm.json)
