from fastapi import APIRouter, HTTPException

from app.crud.user import update_user
from app.schemas.user import UserOut, UserUpdate

router = APIRouter()


@router.put("/{user_id}", response_model=UserOut)
async def admin_update_user(user_id: str, user: UserUpdate):
    db_user = await update_user(user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return UserOut(**db_user.dict())
