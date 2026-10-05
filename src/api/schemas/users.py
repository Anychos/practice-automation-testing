from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, RootModel


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"


class BaseUserResponseSchema(BaseModel):
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


class UpdateUserRequestSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    role: UserRole | None = None


class UpdateUserResponseSchema(BaseUserResponseSchema):
    pass
