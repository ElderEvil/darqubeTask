from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError

from app.auth.security import SECRET_KEY, ALGORITHM
from app.crud.user import get_user_by_email
from app.schemas.token import TokenPayload
from app.schemas.user import UserOut, UserInDB

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login/access-token",
)


async def get_current_user(
        token: str = Depends(reusable_oauth2),
) -> UserOut:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from e
    user = await get_user_by_email(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_admin(current_user: UserInDB = Depends(get_current_user)) -> UserInDB:
    if not current_user.role.value == "admin":
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges",
        )
    return current_user
