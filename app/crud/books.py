from bson.objectid import ObjectId

import sys
sys.path.append("..")

from app.db.mongodb import AsyncIOMotorClient
from ..core.config import settings


book_collection = settings.BOOKS_COLLECTION


def book_helper(book) -> dict:
    return {
        "id": str(book["_id"]),
        "name": book["name"],
        "author": book["author"],
        "release_time": book["release_time"],
        "summary": book["summary"]
    }


async def retrieve_books(db: AsyncIOMotorClient):
    books = []
    async for book in db[book_collection].find():
        books.append(book_helper(book))
    return books


async def add_book(db: AsyncIOMotorClient, book_data: dict) -> dict:
    book = await db[book_collection].insert_one(book_data)
    new_book = await db[book_collection].find_one({"_id": book.inserted_id})
    return book_helper(new_book)


async def retrieve_book(db: AsyncIOMotorClient, id: str) -> dict:
    book = await db[book_collection].find_one({"_id": ObjectId(id)})
    if book:
        return book_helper(book)


async def update_book(db: AsyncIOMotorClient, id: str, data: dict):
    if len(data) < 1:
        return False
    book = await db[book_collection].find_one({"_id": ObjectId(id)})
    if book:
        updated_book = await db[book_collection].update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_book:
            return True
        return False


async def delete_book(db: AsyncIOMotorClient, id: str):
    book = await db[book_collection].find_one({"_id": ObjectId(id)})
    if book:
        await db[book_collection].delete_one({"_id": ObjectId(id)})
        return True
