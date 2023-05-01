from datetime import timedelta
from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm


from app.auth.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.crud.user import authenticate
from app.schemas.token import Token

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await authenticate(
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.email,
            expires_delta=access_token_expires,
        ),
        "token_type": "bearer",
    }
