from http import HTTPStatus

from src.api.assertions.authorization import assert_register_response
from src.api.assertions.base import assert_status_code
from src.api.clients.authorization import AuthorizationAPIClient
from src.api.fixtures.authorization import RegisteredUserFixture
from src.api.schemas.authorization import (
    LoginRequestSchema,
    LoginResponseSchema,
    RegisterRequestSchema,
    RegisterResponseSchema,
)
from src.api.schemas.users import UserRole


class TestAuthorizationPositive:
    def test_register_new_user_returns_201(
        self, authorization_client: AuthorizationAPIClient
    ) -> None:
        request = RegisterRequestSchema()
        response = authorization_client.register_api(request=request)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.CREATED)
        response_data = RegisterResponseSchema.model_validate_json(response.content)
        assert_register_response(
            request=request, response=response_data, user_role=UserRole.USER
        )

    def test_login_existing_user_returns_200(
        self,
        authorization_client: AuthorizationAPIClient,
        registered_user: RegisteredUserFixture,
    ) -> None:
        request = LoginRequestSchema(
            email=registered_user.email, password=registered_user.password
        )
        response = authorization_client.login_api(request=request)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        LoginResponseSchema.model_validate_json(response.content)


class TestAuthorizationNegative:
    pass
