from httpx import Response

from src.api.clients.base import BaseAPIClient
from src.api.clients.public_client_builder import public_client_builder
from src.api.schemas.authorization import (
    LoginRequestSchema,
    LoginResponseSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)
from src.api.tools.routes import Route


class AuthorizationAPIClient(BaseAPIClient):
    def register_api(self, request: RegisterRequestSchema) -> Response:
        return self.post(url=Route.REGISTER, json=request.model_dump())

    def register(self, request: RegisterRequestSchema) -> RegisterResponseSchema:
        response = self.register_api(request=request)
        return RegisterResponseSchema.model_validate_json(response.content)

    def login_api(self, request: LoginRequestSchema) -> Response:
        return self.post(url=Route.LOGIN, json=request.model_dump())

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        response = self.login_api(request=request)
        return LoginResponseSchema.model_validate_json(response.content)


def get_authorization_client() -> AuthorizationAPIClient:
    return AuthorizationAPIClient(client=public_client_builder())
