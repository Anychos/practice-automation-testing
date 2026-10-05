from httpx import Response

from src.api.clients.authorization import AuthorizationAPIClient
from src.api.clients.base import BaseAPIClient
from src.api.clients.private_client_builder import private_client_builder
from src.api.schemas.authorization import LoginRequestSchema
from src.api.schemas.orders import (
    CancelOrderResponseSchema,
    CreateOrderRequestSchema,
    CreateOrderResponseSchema,
    PayOrderResponseSchema,
)
from src.api.tools.routes import Route


class OrdersAPIClient(BaseAPIClient):
    def create_order_api(self, request: CreateOrderRequestSchema) -> Response:
        return self.post(url=Route.ORDERS, json=request.model_dump())

    def create_order(
        self, request: CreateOrderRequestSchema
    ) -> CreateOrderResponseSchema:
        response = self.create_order_api(request=request)
        return CreateOrderResponseSchema.model_validate_json(response.content)

    def get_orders_list_api(self) -> Response:
        return self.get(url=Route.ORDERS)

    def get_order_api(self, order_id: int) -> Response:
        return self.get(url=f"{Route.ORDERS}/{order_id}")

    def cancel_order_api(self, order_id: int) -> Response:
        return self.post(url=f"{Route.ORDERS}/{order_id}")

    def cancel_order(self, order_id: int) -> CancelOrderResponseSchema:
        response = self.cancel_order_api(order_id=order_id)
        return CancelOrderResponseSchema.model_validate_json(response.content)

    def pay_order_api(self, order_id: int) -> Response:
        return self.post(url=f"{Route.ORDERS}/{order_id}")

    def pay_order(self, order_id: int) -> PayOrderResponseSchema:
        response = self.pay_order_api(order_id=order_id)
        return PayOrderResponseSchema.model_validate_json(response.content)


def get_orders_client(
    authorization_client: AuthorizationAPIClient, login_data: LoginRequestSchema
) -> OrdersAPIClient:
    return OrdersAPIClient(
        private_client_builder(
            authorization_client=authorization_client, login_data=login_data
        )
    )
