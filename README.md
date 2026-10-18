# OAuth 2.0 / OIDC Token Verification API

A FastAPI service for the course token-verification challenge.

## Configuration

- Endpoint: `POST /verify`
- Request JSON: `{"token": "<JWT string>"}`
- Allowed JWT algorithm: `RS256` only
- Issuer (`iss`): `https://idp.exam.local`
- Audience (`aud`): `tds-jxbymx1d.apps.exam.local`
- Required claims: `exp`, `iss`, and `aud`

Valid tokens return HTTP 200 with `valid: true` and the verified `email`, `sub`, and `aud` claims. Invalid, expired, tampered, or wrong-issuer/wrong-audience tokens return HTTP 401 with `{"valid": false}`.

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Test the health route at `/` and submit a JSON POST to `/verify`.

## Render deployment

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

After deployment, submit the full endpoint URL including `/verify`.
