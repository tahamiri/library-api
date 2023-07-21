from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
sys.path.append("..")

from app.core import utills
from app.api.api import api_router
from app.core.config import settings
from app.db.mongodb_utills import close_mongo_connection, connect_to_mongo


app = FastAPI()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_event_handler("startup", utills.create_start_app_handler(app))
app.add_event_handler("shutdown", utills.create_stop_app_handler(app))

app.include_router(api_router)
