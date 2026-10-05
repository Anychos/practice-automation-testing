from httpx import Response

from src.api.clients.authorization import AuthorizationAPIClient
from src.api.clients.base import BaseAPIClient
from src.api.clients.private_client_builder import private_client_builder
from src.api.schemas.authorization import LoginRequestSchema
from src.api.schemas.products import (
    CreateProductRequestSchema,
    CreateProductResponseSchema,
    GetProductsListQueryParamsSchema,
    UpdateProductRequestSchema,
)
from src.api.tools.routes import Route


class ProductsAPIClient(BaseAPIClient):
    def create_product_api(self, request: CreateProductRequestSchema) -> Response:
        return self.post(url=Route.PRODUCTS, json=request.model_dump(mode="json"))

    def create_product(
        self, request: CreateProductRequestSchema
    ) -> CreateProductResponseSchema:
        response = self.create_product_api(request=request)
        return CreateProductResponseSchema.model_validate_json(response.content)

    def get_products_list_api(
        self, params: GetProductsListQueryParamsSchema | None = None
    ) -> Response:
        return self.get(
            url=Route.PRODUCTS, params=params.model_dump(mode="json", exclude_none=True)
        )

    def get_product_api(self, product_id: int) -> Response:
        return self.get(url=f"{Route.PRODUCTS}/{product_id}")

    def update_product_api(
        self, product_id: int, request: UpdateProductRequestSchema
    ) -> Response:
        return self.put(
            url=f"{Route.PRODUCTS}/{product_id}", json=request.model_dump(mode="json")
        )

    def delete_product_api(self, product_id: int) -> Response:
        return self.delete(url=f"{Route.PRODUCTS}/{product_id}")


def get_products_client(
    authorization_client: AuthorizationAPIClient, login_data: LoginRequestSchema
) -> ProductsAPIClient:
    return ProductsAPIClient(
        client=private_client_builder(
            authorization_client=authorization_client, login_data=login_data
        )
    )
