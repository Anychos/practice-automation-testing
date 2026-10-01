from src.api.assertions.base import assert_field_value
from src.api.schemas.authorization import RegisterResponseSchema
from src.api.schemas.users import (
    BaseUserResponseSchema,
    GetUserMeResponseSchema,
    GetUserResponseSchema,
    GetUsersResponseSchema,
    UpdateUserRequestSchema,
    UpdateUserResponseSchema,
)


def _assert_user(
    actual: BaseUserResponseSchema, expected: BaseUserResponseSchema
) -> None:
    assert_field_value(actual=actual.id, expected=expected.id, field_name="user_id")
    assert_field_value(actual=actual.email, expected=expected.email, field_name="email")
    assert_field_value(actual=actual.name, expected=expected.name, field_name="name")
    assert_field_value(actual=actual.role, expected=expected.role, field_name="role")


def assert_get_user_me_response(
    *,
    registered_user_response: RegisterResponseSchema,
    get_user_response: GetUserMeResponseSchema,
) -> None:
    _assert_user(actual=get_user_response, expected=registered_user_response)


def assert_get_user_response(
    *,
    registered_user_response: RegisterResponseSchema,
    get_user_response: GetUserResponseSchema,
) -> None:
    _assert_user(actual=get_user_response, expected=registered_user_response)


def assert_user_in_users_response(
    *,
    registered_user_response: RegisterResponseSchema,
    get_users_response: GetUsersResponseSchema,
) -> None:
    actual_user = None

    for user in get_users_response.root:
        if user.id == registered_user_response.id:
            actual_user = user
            break

    assert actual_user is not None, (
        f"Пользователь с id '{registered_user_response.id}' отсутствует в ответе"
    )

    _assert_user(actual=actual_user, expected=registered_user_response)


def assert_update_user_response(
    *,
    register_user_response: RegisterResponseSchema,
    update_user_request: UpdateUserRequestSchema,
    updated_user_response: UpdateUserResponseSchema,
) -> None:
    assert_field_value(
        actual=updated_user_response.id,
        expected=register_user_response.id,
        field_name="id",
    )
    assert_field_value(
        actual=updated_user_response.email,
        expected=register_user_response.email,
        field_name="email",
    )

    if "name" in update_user_request.model_fields_set:
        assert_field_value(
            actual=updated_user_response.name,
            expected=update_user_request.name,
            field_name="name",
        )

    if "role" in update_user_request.model_fields_set:
        assert_field_value(
            actual=updated_user_response.role,
            expected=update_user_request.role,
            field_name="role",
        )
