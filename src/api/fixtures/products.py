from collections.abc import Generator

import pytest
from pydantic import BaseModel

from config import settings
from src.api.clients.authorization import AuthorizationAPIClient
from src.api.clients.products import ProductsAPIClient, get_products_client
from src.api.schemas.authorization import LoginRequestSchema
from src.api.schemas.products import (
    CreateProductRequestSchema,
    CreateProductResponseSchema,
)


class CreatedProductFixture(BaseModel):
    request: CreateProductRequestSchema
    response: CreateProductResponseSchema

    @property
    def id(self) -> int:
        return self.response.id


@pytest.fixture
def user_products_client(
    authorization_client: AuthorizationAPIClient, registered_user: LoginRequestSchema
) -> Generator[ProductsAPIClient, None, None]:
    user_data = LoginRequestSchema(
        email=registered_user.email, password=registered_user.password
    )
    client = get_products_client(
        authorization_client=authorization_client, login_data=user_data
    )

    yield client

    client.close()


@pytest.fixture
def admin_products_client(
    authorization_client: AuthorizationAPIClient,
) -> Generator[ProductsAPIClient, None, None]:
    admin_data = LoginRequestSchema(
        email=settings.admin_login_data.email,
        password=settings.admin_login_data.password,
    )
    client = get_products_client(
        authorization_client=authorization_client, login_data=admin_data
    )

    yield client

    client.close()


@pytest.fixture
def create_product(admin_products_client: ProductsAPIClient) -> CreatedProductFixture:
    request = CreateProductRequestSchema()
    response = admin_products_client.create_product(request=request)
    return CreatedProductFixture(request=request, response=response)


@pytest.fixture
def delete_product(
    admin_products_client: ProductsAPIClient, create_product: CreatedProductFixture
) -> None:
    admin_products_client.delete_product_api(product_id=create_product.id)
