from httpx import Response

from src.api.clients.authorization import AuthorizationAPIClient
from src.api.clients.base import BaseAPIClient
from src.api.clients.private_client_builder import private_client_builder
from src.api.schemas.authorization import LoginRequestSchema
from src.api.schemas.users import UpdateUserRequestSchema
from src.api.tools.routes import Route


class UsersAPIClient(BaseAPIClient):
    def get_user_me_api(self) -> Response:
        return self.get(url=f"{Route.USERS}/me")

    def get_users_api(self) -> Response:
        return self.get(url=Route.USERS)

    def get_user_api(self, user_id: int) -> Response:
        return self.get(url=f"{Route.USERS}/{user_id}")

    def update_user_api(
        self, user_id: int, request: UpdateUserRequestSchema
    ) -> Response:
        return self.patch(
            url=f"{Route.USERS}/{user_id}", json=request.model_dump(exclude_unset=True)
        )

    def delete_user_api(self, user_id: int) -> Response:
        return self.delete(url=f"{Route.USERS}/{user_id}")


def get_users_client(
    authorization_client: AuthorizationAPIClient, login_data: LoginRequestSchema
) -> UsersAPIClient:
    return UsersAPIClient(
        client=private_client_builder(
            authorization_client=authorization_client, login_data=login_data
        )
    )
