from collections.abc import Generator

import pytest

from config import settings
from src.api.clients.authorization import AuthorizationAPIClient
from src.api.clients.users import UsersAPIClient, get_users_client
from src.api.fixtures.authorization import RegisteredUserFixture
from src.api.schemas.authorization import LoginRequestSchema


@pytest.fixture
def user_users_client(
    authorization_client: AuthorizationAPIClient, registered_user: RegisteredUserFixture
) -> Generator[UsersAPIClient, None, None]:
    user_data = LoginRequestSchema(
        email=registered_user.email, password=registered_user.password
    )
    client = get_users_client(
        authorization_client=authorization_client, login_data=user_data
    )

    yield client

    client.close()


@pytest.fixture
def admin_users_client(
    authorization_client: AuthorizationAPIClient,
) -> Generator[UsersAPIClient, None, None]:
    admin_data = LoginRequestSchema(
        email=settings.admin_login_data.email,
        password=settings.admin_login_data.password,
    )
    client = get_users_client(
        authorization_client=authorization_client, login_data=admin_data
    )

    yield client

    client.close()


@pytest.fixture
def delete_user(
    admin_users_client: UsersAPIClient, registered_user: RegisteredUserFixture
) -> None:
    admin_users_client.delete_user_api(user_id=registered_user.user_id)
