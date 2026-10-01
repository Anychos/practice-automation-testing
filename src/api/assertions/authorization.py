from src.api.assertions.base import assert_field_value
from src.api.schemas.authorization import RegisterRequestSchema, RegisterResponseSchema
from src.api.schemas.users import UserRole


def assert_register_response(
    request: RegisterRequestSchema,
    response: RegisterResponseSchema,
    user_role: UserRole,
) -> None:
    assert_field_value(
        actual=response.email, expected=request.email, field_name="email"
    )
    assert_field_value(actual=response.name, expected=request.name, field_name="name")

    assert_field_value(actual=response.role, expected=user_role, field_name="role")
