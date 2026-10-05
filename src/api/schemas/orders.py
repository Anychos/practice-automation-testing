from enum import StrEnum

from pydantic import BaseModel, Field, RootModel


class OrderStatus(StrEnum):
    CREATED = "created"
    PAYMENT_PENDING = "payment_pending"
    PAID = "paid"
    PAYMENT_FAILED = "payment_failed"
    CANCELED = "canceled"


class ItemSchema(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, default=1)


class ItemInOrderSchema(ItemSchema):
    price: float = Field(ge=0)


class OrderSchema(BaseModel):
    id: int = Field(gt=0)
    status: OrderStatus
    total_price: float = Field(ge=0)
    items: list[ItemInOrderSchema]


class CreateOrderRequestSchema(BaseModel):
    items: list[ItemSchema]


class CreateOrderResponseSchema(OrderSchema):
    pass


class GetOrdersResponseSchema(RootModel[list[OrderSchema]]):
    pass


class GetOrderResponseSchema(OrderSchema):
    pass


class CancelOrderResponseSchema(OrderSchema):
    pass


class PayOrderResponseSchema(OrderSchema):
    pass
