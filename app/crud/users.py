from bson.objectid import ObjectId

import sys
sys.path.append("..")

from app.db.mongodb import AsyncIOMotorClient
from ..core.config import settings


user_collection = settings.USERS_COLLECTION


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"]
    }


async def retrieve_users(db: AsyncIOMotorClient):
    users = []
    async for user in db[user_collection].find():
        users.append(user_helper(user))
    return users


async def add_user(db: AsyncIOMotorClient, user_data: dict) -> dict:
    user = await db[user_collection].insert_one(user_data)
    new_user = await db[user_collection].find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def retrieve_user(db: AsyncIOMotorClient, id: str) -> dict:
    user = await db[user_collection].find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


async def update_user(db: AsyncIOMotorClient, id: str, data: dict):
    if len(data) < 1:
        return False
    user = await db[user_collection].find_one({"_id": ObjectId(id)})
    if user:
        updated_book = await db[user_collection].update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_book:
            return True
        return False


async def delete_user(db: AsyncIOMotorClient, id: str):
    user = await db[user_collection].find_one({"_id": ObjectId(id)})
    if user:
        await db[user_collection].delete_one({"_id": ObjectId(id)})
        return True


async def login_user(db: AsyncIOMotorClient, user_data: dict) -> dict:
    user = await db[user_collection].find_one(user_data)
    if user:
        return user_helper(user)
