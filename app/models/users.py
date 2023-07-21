from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "John Doe",
                "email": "jdoe@x.edu.ng",
                "password": "pass"
            }
        }


class UpdateUserModel(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "username": "John Doe",
                "email": "jdoe@x.edu.ng",
                "password": "pass"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
