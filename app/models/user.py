from datetime import datetime
from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, validator


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserRole(str, Enum):
    ADMIN = 'admin'
    DEV = 'dev'
    SIMPLE_MORTAL = 'simple mortal'


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    role: UserRole
    username: str


class UserIn(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        assert len(v) >= 8, 'Password must be at least 8 characters'
        return v


class UserOut(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    is_active: bool
    created_at: datetime
    last_login: datetime

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserInDB(UserOut):
    hashed_password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
