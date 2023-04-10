from fastapi import APIRouter, HTTPException

from app.crud.user import (create_user, get_user, get_all_users, update_user, delete_user)
from app.models.user import UserIn, UserOut, UserUpdate

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
async def create_new_user(user: UserIn) -> UserOut:
    db_user = await create_user(user)
    return UserOut(**db_user.dict())


# @router.post("/login", response_model=UserOut, status_code=201)
# async def login(user: UserLogin):
#     # authenticate_user
#     user_dict = db.get(user.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = get_(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")


@router.get("/{user_id}", response_model=UserOut)
async def get_user_by_id(user_id: str):
    user = get_user(user_id)
    if user is None:
        raise HTTPException(status_code=400, detail=f"There is no user with id {user_id}")


@router.get("/", response_model=list[UserOut])
async def list_users():
    return await get_all_users()


@router.put("/{user_id}", response_model=UserOut)
async def update_user_by_id(user_id: str, user: UserUpdate):
    db_user = await update_user(user_id, user)


@router.delete("/{user_id}", status_code=204)
async def delete_user_by_id(user_id: str):
    await delete_user(user_id)
