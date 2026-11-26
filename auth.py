import jwt
from config import OIDC_JWKS_URL, OIDC_AUDIENCE, OIDC_ISSUER, ALLOWED_REPOSITORIES, TRUSTED_WORKFLOW
from jwt import PyJWKClient
from jwt.exceptions import PyJWTError, PyJWKClientConnectionError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

jwks_client = PyJWKClient(OIDC_JWKS_URL)
security = HTTPBearer()


def validate(token: str) -> dict:
    sign = jwks_client.get_signing_key_from_jwt(token)

    return jwt.decode(
        token,
        sign.key,
        algorithms=["RS256"],
        audience=OIDC_AUDIENCE,
        issuer=OIDC_ISSUER,
        options={
            "require": ["exp", "iat", "nbf", "sub"]
        }
    )

def authorize(claims: dict) -> bool:
    return (
        claims.get("repostiory_id") in ALLOWED_REPOSITORIES
        and claims.get("job_workflow_ref") == TRUSTED_WORKFLOW
        and claims.get("event_name") == "pull_request"
    )

def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:

    try:
        claims = validate(credentials.credentials)
    except PyJWKClientConnectionError:
        raise HTTPException(503, "Identitiy provider unavailable")
    except PyJWTError:
        raise HTTPException(401, "Invalid token", headers= {"WWW-Authenticate: Bearer"})
    if not authorize(claims):
        raise HTTPException(403, "Unauthorized Access")
    return claims

