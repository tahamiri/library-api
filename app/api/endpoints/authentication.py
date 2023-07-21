from fastapi import APIRouter
from fastapi import Body, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

import sys
sys.path.append("..")
from app.db.mongodb import AsyncIOMotorClient
from app.api.deps.db import get_database
from app.api.deps.auth import AuthSetting
from app.crud.users import (
    add_user,
    delete_user,
    retrieve_users,
    retrieve_user,
    update_user,
    login_user,
)
from app.models.users import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)


router = APIRouter()


@AuthJWT.load_config
def get_config():
    return AuthSetting()


@router.post("/users", response_description="User data added into the database")
async def add_user_data(db: AsyncIOMotorClient = Depends(get_database), user: UserSchema = Body(...)):
    user = jsonable_encoder(user)
    new_user = await add_user(db, user)
    return ResponseModel(new_user, "User added successfully.")


@router.get("/users", response_description="Users retrieved")
async def get_users(db: AsyncIOMotorClient = Depends(get_database)):
    users = await retrieve_users(db)
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/users/{id}", response_description="User data retrieved")
async def get_user_data(id, db: AsyncIOMotorClient = Depends(get_database)):
    user = await retrieve_user(db, id)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.put("/users/{id}")
async def update_user_data(id: str, req: UpdateUserModel = Body(...), db: AsyncIOMotorClient = Depends(get_database)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(db, id, req)
    if updated_user:
        return ResponseModel(
            "User with ID: {} name update is successful".format(id),
            "User name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.delete("/users/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str, db: AsyncIOMotorClient = Depends(get_database)):
    deleted_user = await delete_user(db, id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id), "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )


@router.post('/login/', response_description="Login successful", status_code=200)
def login(user: UserSchema, Authorize: AuthJWT = Depends(), db: AsyncIOMotorClient = Depends(get_database)):
    user = jsonable_encoder(user)
    result = login_user(db, user)
    if result:
        access_token = Authorize.create_access_token(subject=" ")
        refresh_token = Authorize.create_refresh_token(subject=" ")
        response_obj = {"access_token": access_token, "refresh_token": refresh_token}

        return JSONResponse(content=response_obj, status_code=200)
    else:
        return Response(content="Invalid username or password", status_code=401)
