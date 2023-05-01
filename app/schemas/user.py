from datetime import datetime
from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


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
    email: EmailStr = Field(..., unique=True)
    role: UserRole
    is_active: bool = True


class UserIn(UserBase):
    password: str = Field(..., min_length=8, max_length=50)


class UserOut(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: datetime = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserInDB(UserOut):
    hashed_password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    password: Optional[str] = Field(min_length=8, max_length=50)
    email: Optional[EmailStr] = Field(None, unique=True)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    last_login: datetime = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
