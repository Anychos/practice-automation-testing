from enum import StrEnum

from pydantic import BaseModel, Field, RootModel


class OrderStatus(StrEnum):
    CREATED = "created"
    PAYMENT_PENDING = "payment_pending"
    PAID = "paid"
    PAYMENT_FAILED = "payment_failed"
    CANCELED = "canceled"


class ItemInOrderSchema(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)
    price: float


class ItemForAddInOrder(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, default=1)


class BaseOrderResponseSchema(BaseModel):
    id: int = Field(gt=0)
    status: OrderStatus
    total_price: float
    items: list[ItemInOrderSchema]


class CreateOrderRequestSchema(BaseModel):
    items: list[ItemForAddInOrder]


class CreateOrderResponseSchema(BaseOrderResponseSchema):
    pass


class GetOrdersResponseSchema(RootModel[list[BaseOrderResponseSchema]]):
    pass


class GetOrderResponseSchema(BaseOrderResponseSchema):
    pass


class CancelOrderResponseSchema(RootModel[list[BaseOrderResponseSchema]]):
    pass


class PayOrderResponseSchema(BaseOrderResponseSchema):
    pass
