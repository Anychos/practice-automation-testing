from enum import StrEnum

from pydantic import EmailStr, Field, RootModel

from src.api.schemas.base import BaseRequestSchema, BaseResponseSchema


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class BaseUserResponseSchema(BaseResponseSchema):
    id: int = Field(gt=0)
    email: EmailStr
    name: str = Field(min_length=1, max_length=120)
    role: UserRole


class GetUserMeResponseSchema(BaseUserResponseSchema):
    pass


class GetUsersResponseSchema(RootModel[list[BaseUserResponseSchema]]):
    pass


class GetUserResponseSchema(BaseUserResponseSchema):
    pass


class UpdateUserRequestSchema(BaseRequestSchema):
    name: str | None = None
    role: UserRole | None = None


class UpdateUserResponseSchema(BaseUserResponseSchema):
    pass
