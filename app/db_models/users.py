from datetime import datetime

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy import String, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field

from app.setup_db import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    def verify_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)


class SignIn(BaseModel):
    username: str = Field(min_length=6, max_length=100)
    password: str


class SignUp(SignIn):
    email: str
    password_confirmation: str


class UserData(BaseModel):
    id: int
    username: str
    email: str
    registered_at: datetime

    model_config = {
        "from_attributes": True
    }


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    email: str
    exp: datetime
    iat: datetime
