from fastapi import HTTPException

from app.auth.users import get_password_hash
from app.models.user import UserIn, UserOut, UserUpdate
from app.utils.mongodb import db

USERS = db["users"]


async def create_user(user: UserIn) -> UserOut | None:
    user_dict = user.dict()
    user_dict['hashed_password'] = get_password_hash(user_dict.pop('password'))
    result = await USERS.insert_one(user_dict)
    return UserOut(**result)


async def get_user(user_id: str) -> UserOut | None:
    user_dict = await USERS.find_one({'_id': user_id})
    if not user_dict:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return UserOut(**user_dict)


async def get_all_users() -> list[UserOut]:
    users = await USERS.find().to_list(length=1000)
    return [UserOut(**user) for user in users]


async def update_user(user_id: str, user: UserUpdate) -> UserOut | None:
    user_dict = user.dict(exclude_unset=True)
    if 'password' in user_dict:
        user_dict['hashed_password'] = get_password_hash(user_dict.pop('password'))
    result = await USERS.update_one({'_id': user_id}, {'$set': user_dict})
    if not result.modified_count:
        raise HTTPException(status_code=400, detail=f"Could not modify user {user_id}")
    updated_user = await USERS.find_one({'_id': user_id})
    return UserOut(**updated_user)


async def delete_user(user_id: str):
    delete_result = await USERS.delete_one({'_id': user_id})
    if not delete_result.deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user_id
