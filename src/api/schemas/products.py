from pydantic import BaseModel, ConfigDict, Field, HttpUrl, RootModel

from src.api.tools.data_generator import fake


class BaseProductSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=120)
    description: str
    image_url: HttpUrl | None
    price: float
    stock_quantity: int
    is_available: bool


class BaseProductResponseSchema(BaseProductSchema):
    id: int = Field(gt=0)


class CreateProductRequestSchema(BaseProductSchema):
    name: str = Field(min_length=1, max_length=120, default_factory=fake.product_name)
    description: str = ""
    image_url: HttpUrl | None = None
    price: float = Field(default_factory=fake.price)
    stock_quantity: int = Field(default_factory=fake.quantity)
    is_available: bool = True


class CreateProductResponseSchema(BaseProductResponseSchema):
    pass


class GetProductResponseSchema(BaseProductResponseSchema):
    pass


class GetProductsListResponseSchema(RootModel[list[BaseProductResponseSchema]]):
    pass


class UpdateProductRequestSchema(CreateProductRequestSchema):
    name: str = Field(min_length=1, max_length=120, default_factory=fake.product_name)
    description: str = Field(default_factory=fake.product_description)
    image_url: HttpUrl | None = None
    price: float = Field(default_factory=fake.price)
    stock_quantity: int = Field(default_factory=fake.quantity)
    is_available: bool = True


class UpdateProductResponseSchema(BaseProductResponseSchema):
    pass


class GetProductsListQueryParamsSchema(BaseModel):
    is_available: bool | None = None
    name: str | None = None
    min_price: float | None = Field(ge=0, le=9999999.99, default=None)
    max_price: float | None = Field(ge=0, le=9999999.99, default=None)
    limit: int = Field(ge=1, le=100, default=20)
    offset: int = Field(ge=0, default=0)
