from http import HTTPStatus

import pytest

from src.api.assertions.base import assert_status_code
from src.api.assertions.orders import (
    assert_cancel_order_response,
    assert_create_order_response,
    assert_get_order_response,
    assert_get_orders_list_response,
    assert_pay_order_response,
)
from src.api.clients.orders import OrdersAPIClient
from src.api.fixtures.orders import CreatedOrderFixture
from src.api.fixtures.products import CreatedProductFixture
from src.api.schemas.orders import (
    CancelOrderResponseSchema,
    CreateOrderRequestSchema,
    CreateOrderResponseSchema,
    GetOrderResponseSchema,
    GetOrdersResponseSchema,
    ItemSchema,
    PayOrderResponseSchema,
)


@pytest.mark.orders
@pytest.mark.regression
class TestOrdersPositive:
    @pytest.mark.smoke
    def test_user_create_order_returns_201(
        self,
        user_orders_client: OrdersAPIClient,
        create_product: CreatedProductFixture,
    ) -> None:
        request = CreateOrderRequestSchema(
            items=[ItemSchema(product_id=create_product.id)]
        )
        response = user_orders_client.create_order_api(request=request)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.CREATED)
        response_data = CreateOrderResponseSchema.model_validate_json(response.content)
        assert_create_order_response(
            create_order_request=request,
            create_order_response=response_data,
        )

    @pytest.mark.smoke
    def test_user_get_existing_order_returns_200(
        self,
        user_orders_client: OrdersAPIClient,
        create_order: CreatedOrderFixture,
    ) -> None:
        response = user_orders_client.get_order_api(order_id=create_order.id)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        response_data = GetOrderResponseSchema.model_validate_json(response.content)
        assert_get_order_response(
            create_order_response=create_order.response,
            get_order_response=response_data,
        )

    @pytest.mark.smoke
    def test_user_get_orders_list_returns_200(
        self,
        user_orders_client: OrdersAPIClient,
        create_order: CreatedOrderFixture,
    ) -> None:
        response = user_orders_client.get_orders_list_api()

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        response_data = GetOrdersResponseSchema.model_validate_json(response.content)
        assert_get_orders_list_response(
            create_order_response=create_order.response,
            get_orders_response=response_data,
        )

    @pytest.mark.smoke
    def test_user_cancel_order_returns_200(
        self,
        user_orders_client: OrdersAPIClient,
        create_order: CreatedOrderFixture,
    ) -> None:
        response = user_orders_client.cancel_order_api(order_id=create_order.id)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        response_data = CancelOrderResponseSchema.model_validate_json(response.content)
        assert_cancel_order_response(
            create_order_response=create_order.response,
            cancel_order_response=response_data,
        )

    @pytest.mark.smoke
    def test_user_pay_order_returns_200(
        self,
        user_orders_client: OrdersAPIClient,
        create_order: CreatedOrderFixture,
    ) -> None:
        response = user_orders_client.pay_order_api(order_id=create_order.id)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        response_data = PayOrderResponseSchema.model_validate_json(response.content)
        assert_pay_order_response(
            create_order_response=create_order.response,
            pay_order_response=response_data,
        )


class TestOrdersNegative:
    pass
