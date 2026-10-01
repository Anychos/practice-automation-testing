from httpx import Client

from config import settings
from src.api.clients.authorization import AuthorizationAPIClient
from src.api.schemas.authorization import LoginRequestSchema


def private_client_builder(
    *, authorization_client: AuthorizationAPIClient, login_data: LoginRequestSchema
) -> Client:
    login_response = authorization_client.login(request=login_data)

    return Client(
        base_url=settings.http_client.url,
        timeout=settings.http_client.timeout,
        headers={"Authorization": f"Bearer {login_response.access_token}"},
    )
