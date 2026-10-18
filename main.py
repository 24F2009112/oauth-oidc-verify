from typing import Any

import jwt
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

ISSUER = "https://idp.exam.local"
AUDIENCE = "tds-jxbymx1d.apps.exam.local"

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuY
cxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMID
EkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXc
WyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfW
ed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfI
SI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIX
dQIDAQAB
-----END PUBLIC KEY-----"""

app = FastAPI(title="OAuth 2.0 / OIDC Token Verification Service", version="1.0.0")


class VerifyRequest(BaseModel):
    token: str = Field(..., min_length=1)


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "token-verification", "endpoint": "POST /verify"}


@app.post("/verify")
def verify_token(body: VerifyRequest) -> Any:
    """Validate the JWT signature, issuer, audience, and expiry."""
    try:
        claims = jwt.decode(
            body.token,
            key=PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={"require": ["exp", "iss", "aud"]},
        )
    except (jwt.InvalidTokenError, TypeError, ValueError):
        return JSONResponse(status_code=401, content={"valid": False})

    # Return the claim values from the verified token rather than constants.
    result = {
        "valid": True,
        "email": claims.get("email", ""),
        "sub": claims.get("sub", ""),
        "aud": claims.get("aud", ""),
    }
    return JSONResponse(status_code=200, content=result)
