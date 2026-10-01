from collections.abc import Generator

import pytest
from pydantic import BaseModel, EmailStr

from src.api.clients.authorization import (
    AuthorizationAPIClient,
    get_authorization_client,
)
from src.api.schemas.authorization import RegisterRequestSchema, RegisterResponseSchema


class RegisteredUserFixture(BaseModel):
    request: RegisterRequestSchema
    response: RegisterResponseSchema

    @property
    def email(self) -> EmailStr:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

    @property
    def user_id(self) -> int:
        return self.response.id


@pytest.fixture(scope="function")
def authorization_client() -> Generator[AuthorizationAPIClient, None, None]:
    client = get_authorization_client()

    yield client

    client.close()


@pytest.fixture(scope="function")
def registered_user(
    authorization_client: AuthorizationAPIClient,
) -> RegisteredUserFixture:
    request = RegisterRequestSchema()
    response = authorization_client.register(request=request)
    return RegisteredUserFixture(request=request, response=response)
