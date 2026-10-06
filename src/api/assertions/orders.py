from collections.abc import Sequence

from src.api.assertions.base import assert_field_value
from src.api.schemas.orders import (
    CancelOrderResponseSchema,
    CreateOrderRequestSchema,
    CreateOrderResponseSchema,
    GetOrderResponseSchema,
    GetOrdersResponseSchema,
    ItemSchema,
    OrderSchema,
    OrderStatus,
    PayOrderResponseSchema,
)


def _assert_order_items(
    *,
    expected_items: Sequence[ItemSchema],
    actual_order: OrderSchema,
) -> None:
    assert_field_value(
        actual=len(actual_order.items),
        expected=len(expected_items),
        field_name="items count",
    )

    for index, (expected_item, actual_item) in enumerate(
        zip(expected_items, actual_order.items, strict=True)
    ):
        assert_field_value(
            actual=actual_item.product_id,
            expected=expected_item.product_id,
            field_name=f"items[{index}].product_id",
        )
        assert_field_value(
            actual=actual_item.quantity,
            expected=expected_item.quantity,
            field_name=f"items[{index}].quantity",
        )


def _assert_same_order(
    *, expected_order: OrderSchema, actual_order: OrderSchema
) -> None:
    assert_field_value(
        actual=actual_order.id,
        expected=expected_order.id,
        field_name="id",
    )
    assert_field_value(
        actual=actual_order.status,
        expected=expected_order.status,
        field_name="status",
    )
    _assert_order_items(
        expected_items=expected_order.items,
        actual_order=actual_order,
    )


def assert_create_order_response(
    *,
    create_order_request: CreateOrderRequestSchema,
    create_order_response: CreateOrderResponseSchema,
) -> None:
    assert_field_value(
        actual=create_order_response.status,
        expected=OrderStatus.CREATED,
        field_name="status",
    )
    _assert_order_items(
        expected_items=create_order_request.items,
        actual_order=create_order_response,
    )


def assert_get_order_response(
    *,
    create_order_response: CreateOrderResponseSchema,
    get_order_response: GetOrderResponseSchema,
) -> None:
    _assert_same_order(
        expected_order=create_order_response,
        actual_order=get_order_response,
    )


def assert_get_orders_list_response(
    *,
    create_order_response: CreateOrderResponseSchema,
    get_orders_response: GetOrdersResponseSchema,
) -> None:
    actual_order = next(
        (
            order
            for order in get_orders_response.root
            if order.id == create_order_response.id
        ),
        None,
    )

    assert actual_order is not None, (
        f"Заказ с id '{create_order_response.id}' отсутствует в ответе"
    )
    _assert_same_order(
        expected_order=create_order_response,
        actual_order=actual_order,
    )


def assert_cancel_order_response(
    *,
    create_order_response: CreateOrderResponseSchema,
    cancel_order_response: CancelOrderResponseSchema,
) -> None:
    assert_field_value(
        actual=cancel_order_response.id,
        expected=create_order_response.id,
        field_name="id",
    )
    assert_field_value(
        actual=cancel_order_response.status,
        expected=OrderStatus.CANCELED,
        field_name="status",
    )
    _assert_order_items(
        expected_items=create_order_response.items,
        actual_order=cancel_order_response,
    )


def assert_pay_order_response(
    *,
    create_order_response: CreateOrderResponseSchema,
    pay_order_response: PayOrderResponseSchema,
) -> None:
    assert_field_value(
        actual=pay_order_response.id,
        expected=create_order_response.id,
        field_name="id",
    )
    allowed_statuses = (OrderStatus.PAYMENT_PENDING, OrderStatus.PAID)
    assert pay_order_response.status in allowed_statuses, (
        "Некорректный статус заказа после запуска оплаты. "
        f"Ожидается один из статусов {allowed_statuses!r}, "
        f"получено {pay_order_response.status!r}."
    )
    _assert_order_items(
        expected_items=create_order_response.items,
        actual_order=pay_order_response,
    )
