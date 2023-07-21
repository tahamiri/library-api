from pydantic import BaseModel
from app.core.config import settings


secret_key = settings.SECRET_KEY


class AuthSetting(BaseModel):
    authjwt_secret_key: str = secret_key
