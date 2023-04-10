from fastapi import APIRouter, Depends, HTTPException

from app.crud.user import update_user
from app.models.user import UserOut, UserUpdate

admin_router = APIRouter()


@admin_router.put("/{user_id}", response_model=UserOut)
async def admin_update_user_by_id(user_id: str, user: UserUpdate):
    db_user = await update_user(user_id, user)
    if db_user:
        return UserOut(**db_user.dict())
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
