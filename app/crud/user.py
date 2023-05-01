from datetime import datetime
from typing import Optional

from bson import ObjectId
from fastapi import HTTPException

from app.auth.security import get_password_hash, verify_password
from app.db.mongodb import users_collection
from app.schemas.user import UserIn, UserOut, UserUpdate, UserInDB


async def create_user(user: UserIn) -> UserOut | None:
    user_dict = user.dict()
    user_dict['hashed_password'] = get_password_hash(user_dict.pop('password'))
    await users_collection.insert_one(user_dict)
    return UserOut(**user_dict)


async def get_user(user_id: str) -> UserOut | None:
    user_dict = await users_collection.find_one({'_id': ObjectId(user_id)})
    if not user_dict:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return UserOut(**user_dict)


async def get_all_users(limit: int) -> list[UserOut]:
    users = await users_collection.find().to_list(length=limit)
    return [UserOut(**user) for user in users]


async def update_user(user_id: str, user: UserUpdate) -> UserOut | None:
    user_dict = user.dict(exclude_unset=True)
    if 'password' in user_dict:
        user_dict['hashed_password'] = get_password_hash(user_dict.pop('password'))
    result = await users_collection.update_one({'_id': ObjectId(user_id)}, {'$set': user_dict})
    if not result.modified_count:
        raise HTTPException(status_code=400, detail=f"Could not modify user {user_id}")
    updated_user = await users_collection.find_one({'_id': ObjectId(user_id)})
    return UserOut(**updated_user)


async def delete_user(user_id: str):
    delete_result = await users_collection.delete_one({'_id': ObjectId(user_id)})
    if not delete_result.deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user_id


async def get_user_by_email(email: str) -> UserInDB:
    user_dict = await users_collection.find_one({'email': email})
    if not user_dict:
        raise HTTPException(status_code=404, detail=f"User with email: {email} not found")
    return UserInDB(**user_dict)


async def authenticate(email: str, password: str) -> Optional[UserOut]:
    user = await get_user_by_email(email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    result = await users_collection.update_one({'_id': ObjectId(user.id)}, {'$set': {'last_login': datetime.utcnow()}})
    if not result.modified_count:
        raise HTTPException(status_code=400, detail=f"Could not modify user {email}")
    return user
