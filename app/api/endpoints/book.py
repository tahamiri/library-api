from fastapi import APIRouter
from fastapi import Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

import sys
sys.path.append("..")

from app.db.mongodb import AsyncIOMotorClient
from app.api.deps.db import get_database
from app.api.deps.auth import AuthSetting
from app.crud.books import (
    add_book,
    delete_book,
    retrieve_books,
    retrieve_book,
    update_book,
)
from app.models.users import (
    ErrorResponseModel,
    ResponseModel,
)
from app.models.books import (
    BookSchema,
    UpdateBookModel,
)


router = APIRouter()


@AuthJWT.load_config
def get_config():
    return AuthSetting()


@router.post("/books", response_description="Book data added into the database")
async def add_book_data(book: BookSchema = Body(...), Authorize: AuthJWT = Depends(), db: AsyncIOMotorClient = Depends(get_database)):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")
    book = jsonable_encoder(book)
    new_book = await add_book(db, book)
    return ResponseModel(new_book, "Book added successfully.")


@router.get("/books", response_description="Books retrieved")
async def get_books(Authorize: AuthJWT = Depends(), db: AsyncIOMotorClient = Depends(get_database)):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")
    books = await retrieve_books(db)
    if books:
        return ResponseModel(books, "Books data retrieved successfully")
    return ResponseModel(books, "Empty list returned")


@router.get("/books/{id}", response_description="Book data retrieved")
async def get_book_data(id, Authorize: AuthJWT = Depends(), db: AsyncIOMotorClient = Depends(get_database)):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")
    book = await retrieve_book(db, id)
    if book:
        return ResponseModel(book, "Book data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Book doesn't exist.")


@router.put("/books/{id}")
async def update_book_data(id: str, req: UpdateBookModel = Body(...), Authorize: AuthJWT = Depends(), db: AsyncIOMotorClient = Depends(get_database)):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_book = await update_book(db, id, req)
    if updated_book:
        return ResponseModel(
            "Book with ID: {} name update is successful".format(id),
            "Book name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the book data.",
    )


@router.delete("/books/{id}", response_description="Book data deleted from the database")
async def delete_book_data(id: str, Authorize: AuthJWT = Depends(), db: AsyncIOMotorClient = Depends(get_database)):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")
    deleted_book = await delete_book(db, id)
    if deleted_book:
        return ResponseModel(
            "Book with ID: {} removed".format(id), "Book deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Book with id {0} doesn't exist".format(id)
    )
