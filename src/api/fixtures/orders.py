from collections.abc import Generator

import pytest
from pydantic import BaseModel

from config import settings
from src.api.clients.authorization import AuthorizationAPIClient
from src.api.clients.orders import OrdersAPIClient, get_orders_client
from src.api.fixtures.products import CreatedProductFixture
from src.api.schemas.authorization import LoginRequestSchema
from src.api.schemas.orders import (
    CreateOrderRequestSchema,
    CreateOrderResponseSchema,
    ItemSchema,
)


class CreatedOrderFixture(BaseModel):
    request: CreateOrderRequestSchema
    response: CreateOrderResponseSchema

    @property
    def id(self) -> int:
        return self.response.id


@pytest.fixture
def user_orders_client(
    authorization_client: AuthorizationAPIClient, registered_user: LoginRequestSchema
) -> Generator[OrdersAPIClient, None, None]:
    user_data = LoginRequestSchema(
        email=registered_user.email, password=registered_user.password
    )
    client = get_orders_client(
        authorization_client=authorization_client, login_data=user_data
    )

    yield client

    client.close()


@pytest.fixture
def admin_orders_client(
    authorization_client: AuthorizationAPIClient,
) -> Generator[OrdersAPIClient, None, None]:
    admin_data = LoginRequestSchema(
        email=settings.admin_login_data.email,
        password=settings.admin_login_data.password,
    )
    client = get_orders_client(
        authorization_client=authorization_client, login_data=admin_data
    )

    yield client

    client.close()


@pytest.fixture
def create_order(
    user_orders_client: OrdersAPIClient, create_product: CreatedProductFixture
) -> CreatedOrderFixture:
    request = CreateOrderRequestSchema(items=[ItemSchema(product_id=create_product.id)])
    response = user_orders_client.create_order(request=request)
    return CreatedOrderFixture(request=request, response=response)


@pytest.fixture
def cancel_order(
    user_orders_client: OrdersAPIClient, create_order: CreatedOrderFixture
) -> None:
    user_orders_client.cancel_order(order_id=create_order.id)


@pytest.fixture
def pay_order(
    user_orders_client: OrdersAPIClient, create_order: CreatedOrderFixture
) -> None:
    user_orders_client.pay_order(order_id=create_order.id)
