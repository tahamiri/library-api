from typing import Optional
from pydantic import BaseModel, Field, constr


time_validation = '\d{4}\/\d{2}\/\d{2}'


class BookSchema(BaseModel):
    name: str = Field(...)
    author: str = Field(...)
    release_time: constr(regex=time_validation) = Field(...)
    summary: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "author": "something",
                "release_time": "1398/05/11",
                "summary": "some summary"
            }
        }


class UpdateBookModel(BaseModel):
    name: Optional[str]
    author: Optional[str]
    release_time: Optional[constr(regex=time_validation)]
    summary: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "author": "something",
                "release_time": "1398/05/11",
                "summary": "some summary"
            }
        }
