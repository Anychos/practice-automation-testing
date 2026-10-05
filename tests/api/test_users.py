from http import HTTPStatus

import pytest

from src.api.assertions.base import assert_status_code
from src.api.assertions.users import (
    assert_get_user_me_response,
    assert_get_user_response,
    assert_update_user_response,
    assert_user_in_users_response,
)
from src.api.clients.users import UsersAPIClient
from src.api.fixtures.authorization import RegisteredUserFixture
from src.api.schemas.users import (
    GetUserMeResponseSchema,
    GetUserResponseSchema,
    GetUsersResponseSchema,
    UpdateUserRequestSchema,
    UpdateUserResponseSchema,
)
from src.api.tools.data_generator import fake


@pytest.mark.users
@pytest.mark.regression
class TestUsersPositive:
    @pytest.mark.smoke
    def test_get_current_logged_in_user_returns_200(
        self, registered_user: RegisteredUserFixture, user_users_client: UsersAPIClient
    ) -> None:
        response = user_users_client.get_user_me_api()

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        response_data = GetUserMeResponseSchema.model_validate_json(response.content)
        assert_get_user_me_response(
            registered_user_response=registered_user.response,
            get_user_response=response_data,
        )

    @pytest.mark.smoke
    def test_admin_get_users_list_returns_200(
        self, registered_user: RegisteredUserFixture, admin_users_client: UsersAPIClient
    ) -> None:
        response = admin_users_client.get_users_api()

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        response_data = GetUsersResponseSchema.model_validate_json(response.content)
        assert_user_in_users_response(
            registered_user_response=registered_user.response,
            get_users_response=response_data,
        )

    @pytest.mark.smoke
    def test_admin_get_existing_user_info_returns_200(
        self, registered_user: RegisteredUserFixture, admin_users_client: UsersAPIClient
    ) -> None:
        response = admin_users_client.get_user_api(user_id=registered_user.user_id)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        response_data = GetUserResponseSchema.model_validate_json(response.content)
        assert_get_user_response(
            registered_user_response=registered_user.response,
            get_user_response=response_data,
        )

    @pytest.mark.smoke
    def test_admin_update_user_returns_200(
        self, registered_user: RegisteredUserFixture, admin_users_client: UsersAPIClient
    ) -> None:
        request = UpdateUserRequestSchema(name=fake.username())
        response = admin_users_client.update_user_api(
            user_id=registered_user.user_id, request=request
        )

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        response_data = UpdateUserResponseSchema.model_validate_json(response.content)
        assert_update_user_response(
            register_user_response=registered_user.response,
            update_user_request=request,
            updated_user_response=response_data,
        )

    @pytest.mark.smoke
    def test_delete_user_returns_204(
        self, registered_user: RegisteredUserFixture, admin_users_client: UsersAPIClient
    ) -> None:
        delete_response = admin_users_client.delete_user_api(
            user_id=registered_user.user_id
        )
        assert_status_code(
            actual=delete_response.status_code, expected=HTTPStatus.NO_CONTENT
        )

        get_deleted_user_response = admin_users_client.get_user_api(
            user_id=registered_user.user_id
        )
        assert_status_code(
            actual=get_deleted_user_response.status_code, expected=HTTPStatus.NOT_FOUND
        )


class TestUsersNegative:
    pass
