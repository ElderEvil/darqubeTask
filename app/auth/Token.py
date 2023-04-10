from pydantic import BaseModel


class Token(BaseModel):
    username: str
    hashed_password: str

