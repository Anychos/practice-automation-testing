from typing import Literal

from pydantic import EmailStr, Field

from src.api.schemas.base import BaseRequestSchema, BaseResponseSchema
from src.api.schemas.users import BaseUserResponseSchema
from src.api.tools.data_generator import fake


class RegisterRequestSchema(BaseRequestSchema):
    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(min_length=8, max_length=128, default_factory=fake.password)
    name: str = Field(min_length=1, max_length=120, default_factory=fake.username)


class RegisterResponseSchema(BaseUserResponseSchema):
    pass


class LoginRequestSchema(BaseRequestSchema):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginResponseSchema(BaseResponseSchema):
    access_token: str = Field(min_length=1)
    token_type: Literal["bearer"]
