from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext
from starlette import status
from starlette.requests import Request

from app.auth.Token import Token
from app.models.user import UserInDB, UserRole
from app.utils.mongodb import db

USERS = db["users"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_by_username(username: str) -> UserInDB:
    user_dict = USERS.find_one({"username": username})
    return UserInDB(**user_dict)


async def authenticate_user(credentials: HTTPBasicCredentials) -> UserInDB | None:
    username = credentials.username
    password = credentials.password
    user = get_user_by_username(username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_current_user_token(credentials: HTTPBasicCredentials = Depends()):
    user = await authenticate_user(credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return Token(
        username=user["username"],
        hashed_password=user["hashed_password"],
        is_admin=user.role == UserRole.ADMIN
    )


async def check_is_admin(request: Request):
    if "auth" in request.headers:
        ...
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin permission required")
    return request
