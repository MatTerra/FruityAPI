from typing import Any

from fastapi import Response, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth


async def get_user(response: Response,
                   cred: HTTPAuthorizationCredentials
                   = Depends(HTTPBearer(auto_error=True))):
    if cred is None:
        raise HTTPException(
            status_code=401,
            detail="Bearer authentication required",
            headers={"WWW-Authenticate": 'Bearer realm="auth_required"'}
        )
    try:
        decoded_token = auth.verify_id_token(cred.credentials)
        response.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
        print(decoded_token)
        return decoded_token
    except Exception as err:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials. {err}",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'}
        )

async def optional_get_user(response: Response,
                   cred: HTTPAuthorizationCredentials
                   = Depends(HTTPBearer(auto_error=False))):
    if cred is None:
        return None
    try:
        decoded_token = auth.verify_id_token(cred.credentials)
        response.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
        return decoded_token
    except Exception as err:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication credentials. {err}",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'}
        )
