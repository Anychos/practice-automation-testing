from http import HTTPStatus

import pytest

from src.api.assertions.base import assert_status_code
from src.api.assertions.products import (
    assert_create_product_response,
    assert_get_product_response,
    assert_product_in_products_list_response,
    assert_update_product_response,
)
from src.api.clients.products import ProductsAPIClient
from src.api.fixtures.products import CreatedProductFixture
from src.api.schemas.products import (
    CreateProductRequestSchema,
    CreateProductResponseSchema,
    GetProductResponseSchema,
    GetProductsListQueryParamsSchema,
    GetProductsListResponseSchema,
    UpdateProductRequestSchema,
    UpdateProductResponseSchema,
)


@pytest.mark.products
@pytest.mark.regression
class TestProductsPositive:
    @pytest.mark.smoke
    def test_admin_create_product_returns_201(
        self, admin_products_client: ProductsAPIClient
    ) -> None:
        request = CreateProductRequestSchema()
        response = admin_products_client.create_product_api(request=request)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.CREATED)
        response_data = CreateProductResponseSchema.model_validate_json(
            response.content
        )
        assert_create_product_response(
            create_product_request=request, create_product_response=response_data
        )

    @pytest.mark.smoke
    def test_user_get_existing_product_returns_200(
        self,
        user_products_client: ProductsAPIClient,
        create_product: CreatedProductFixture,
    ) -> None:
        response = user_products_client.get_product_api(product_id=create_product.id)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        response_data = GetProductResponseSchema.model_validate_json(response.content)
        assert_get_product_response(
            create_product_response=create_product.response,
            get_product_response=response_data,
        )

    @pytest.mark.smoke
    def test_user_get_products_list_returns_200(
        self,
        user_products_client: ProductsAPIClient,
        create_product: CreatedProductFixture,
    ) -> None:
        params = GetProductsListQueryParamsSchema(name=create_product.name)
        response = user_products_client.get_products_list_api(params=params)

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        response_data = GetProductsListResponseSchema.model_validate_json(
            response.content
        )
        assert_product_in_products_list_response(
            create_product_response=create_product.response,
            get_products_response=response_data,
        )

    @pytest.mark.smoke
    def test_full_update_product_returns_200(
        self,
        admin_products_client: ProductsAPIClient,
        create_product: CreatedProductFixture,
    ) -> None:
        request = UpdateProductRequestSchema()
        response = admin_products_client.update_product_api(
            request=request, product_id=create_product.id
        )

        assert_status_code(actual=response.status_code, expected=HTTPStatus.OK)
        response_data = UpdateProductResponseSchema.model_validate_json(
            response.content
        )
        assert_update_product_response(
            update_product_request=request, update_product_response=response_data
        )

    @pytest.mark.smoke
    def test_delete_existing_product_returns_204(
        self,
        admin_products_client: ProductsAPIClient,
        create_product: CreatedProductFixture,
    ) -> None:
        response = admin_products_client.delete_product_api(
            product_id=create_product.id
        )

        assert_status_code(actual=response.status_code, expected=HTTPStatus.NO_CONTENT)

        get_deleted_product_response = admin_products_client.get_product_api(
            product_id=create_product.id
        )
        assert_status_code(
            actual=get_deleted_product_response.status_code,
            expected=HTTPStatus.NOT_FOUND,
        )


class TestProductsNegative:
    pass
