from decimal import Decimal

from src.api.assertions.base import assert_field_value
from src.api.schemas.products import (
    BaseProductResponseSchema,
    BaseProductSchema,
    CreateProductRequestSchema,
    CreateProductResponseSchema,
    GetProductResponseSchema,
    GetProductsListResponseSchema,
    UpdateProductRequestSchema,
    UpdateProductResponseSchema,
)


def _assert_product(
    actual: BaseProductResponseSchema,
    expected: BaseProductSchema | BaseProductResponseSchema,
) -> None:
    assert_field_value(actual=actual.name, expected=expected.name, field_name="name")
    assert_field_value(
        actual=actual.description,
        expected=expected.description,
        field_name="description",
    )
    assert_field_value(
        actual=actual.image_url, expected=expected.image_url, field_name="image_url"
    )
    assert_field_value(
        actual=Decimal(actual.price),
        expected=Decimal(str(expected.price)),
        field_name="price",
    )
    assert_field_value(
        actual=actual.stock_quantity,
        expected=expected.stock_quantity,
        field_name="stock_quantity",
    )
    assert_field_value(
        actual=actual.is_available,
        expected=expected.is_available,
        field_name="is_available",
    )


def assert_create_product_response(
    *,
    create_product_request: CreateProductRequestSchema,
    create_product_response: CreateProductResponseSchema,
) -> None:
    _assert_product(actual=create_product_response, expected=create_product_request)


def assert_get_product_response(
    *,
    create_product_response: CreateProductResponseSchema,
    get_product_response: GetProductResponseSchema,
) -> None:
    _assert_product(actual=get_product_response, expected=create_product_response)


def assert_product_in_products_list_response(
    *,
    create_product_response: CreateProductResponseSchema,
    get_products_response: GetProductsListResponseSchema,
) -> None:
    actual_product = None

    for product in get_products_response.root:
        if product.id == create_product_response.id:
            actual_product = product
            break

    assert actual_product is not None, (
        f"Продукт с id '{create_product_response.id}' отсутствует в ответе"
    )

    _assert_product(actual=actual_product, expected=create_product_response)


def assert_update_product_response(
    *,
    update_product_request: UpdateProductRequestSchema,
    update_product_response: UpdateProductResponseSchema,
) -> None:
    _assert_product(actual=update_product_response, expected=update_product_request)
