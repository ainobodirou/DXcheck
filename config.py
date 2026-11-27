import os 

Q_SIZE = int(os.environ.get("QUEUE_SIZE", "100"))
Q_PUT_TIMEOUT = int(os.environ.get("QUEUE_TIMEOUT"), "2")
JOB_TTL = int(os.environ.get("JOB_TTL"), 15)
OIDC_ISSUER = "https://token.actions.githubusercontent.com"
OIDC_AUDIENCE = os.environ["OIDC_AUDIENCE"]
OIDC_JWKS_URL = f"{OIDC_ISSUER}/.well-known/jwks"
ALLOWED_REPOSITORIES = frozenset(
    os.environ["ALLOWED_REPOSITORIES"].split(",")
)
TRUSTED_WORKFLOW_SHA= 

TRUSTED_WORKFLOW = os.environ["TRUSTED_WORKFLOW"]