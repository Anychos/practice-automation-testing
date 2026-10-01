from typing import Any


def assert_field_value(*, actual: Any, expected: Any, field_name: str) -> None:
    assert actual == expected, (
        f"Значение поля '{field_name}' не соответствует ожидаемому."
        f"Ожидается '{expected!r}', получено '{actual!r}'."
    )


def assert_status_code(*, actual: int, expected: int) -> None:
    assert actual == expected, (
        f"Получен некорректный статус код ответа."
        f"Ожидается '{expected}', получен '{actual}'"
    )
