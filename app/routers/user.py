from typing import List

from fastapi import APIRouter

from app.crud.user import (create_user, get_user, update_user, delete_user, get_all_users)
from app.schemas.user import UserIn, UserOut, UserUpdate

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=201)
async def create_new_user(user: UserIn) -> UserOut:
    return await create_user(user)


@router.get("/", response_model=List[UserOut])
async def read_all_users(limit: int = 100):
    return await get_all_users(limit)


@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: str):
    return await get_user(user_id)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: str, user: UserUpdate):
    return await update_user(user_id, user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str):
    return await delete_user(user_id)
