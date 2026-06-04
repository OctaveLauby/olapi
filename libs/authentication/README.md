# authentication

Keycloak authentication client library (src-layout, packaged with `uv_build`).

Exposes a `KeycloakClient` and related exceptions used by workspace apps to
register users, issue tokens, and validate them.

## Use

Declare it as a workspace dependency in a member's `pyproject.toml`:

```toml
dependencies = ["authentication"]

[tool.uv.sources]
authentication = { workspace = true }
```

Then import:

```python
from authentication.keycloak import KeycloakClient
from authentication import exceptions
```
