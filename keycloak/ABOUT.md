# Realm

> Simplified from Claude description.

Keycloak ships with a built-in master realm dedicated to administering Keycloak itself (the admin/admin user lives there). You create separate realms for your applications.

- `"realm": "olapi"`: Realm identifier, appears in URLs (`/realms/olapi/...`) and JWT `iss` claim.
- `"enabled": true`: Kill-switch for the realm
- `"registrationAllowed": false`: Keycloak's built-in self-registration page; off so new users must go through `POST /users`.
- `"clientId": "olapi-api"`: Client identifier the API sends in token requests.
- `"enabled": true`: Kill-switch for the client
- `"protocol": "openid-connect"`: OIDC vs SAML; explicit even though OIDC is the default.
- `"publicClient": true`: Whether the client needs a `client_secret`; on (no secret) — our backend is trusted and it keeps config simpler.
- `"standardFlowEnabled": false`: OAuth2 Authorization Code flow (redirect-based browser login); off, we don't use UI redirects.
- `"implicitFlowEnabled": false`: Legacy Implicit flow (tokens in URL fragment); off — deprecated, always off in modern setups.
- `"directAccessGrantsEnabled": true`: ROPC flow (username/password → token in one POST); on, it's what `POST /login` uses.
