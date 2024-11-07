import os
from datetime import timedelta
from pathlib import Path

from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()

DEV_MODE = os.getenv("DEV_MODE", False)
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)

BASE_DIR = Path(__file__).parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire: timedelta = timedelta(hours=2)


AUTH_JWT_SETTINGS = AuthJWT()


if DEV_MODE:
    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # noqa
else:
    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@db:{DB_PORT}/{DB_NAME}"  # noqa

