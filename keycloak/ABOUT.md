# Realm

- `"realm": "olapi"`: Realm identifier, appears in URLs (`/realms/olapi/...`).
- `"registrationAllowed": false`: disable registration page to enforce registration with api and ensure username=email
- `"registrationEmailAsUsername": true`: forces username=email (username is ignored if given in create)
- `"clients": ...`
    - `"clientId": "olapi-api"`: Client identifier the API sends in token requests.
    - `"protocol": "openid-connect"`: OIDC (modern, uses json - jwt -) vs SAML (older, uses XML); explicit even though OIDC is the default.
    - `"publicClient": true`: Whether the client needs a `client_secret`; on (no secret) — our backend is trusted and it keeps config simpler.
    - `"standardFlowEnabled": false`: OAuth2 Authorization Code flow (redirect-based browser login); off for simplicity but not recommanded.
    - `"directAccessGrantsEnabled": true`: toggles the Resource Owner Password Credentials (ROPC) that we uses for login
- `"components": ...`: Only makes email required to avoid "Account is not fully set up" error message
