from http import HTTPStatus

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app.api import app
from app.config import environment
from app.schemas import Predictions, ProductList

client = TestClient(app)


@pytest.fixture
def sample_products():
    return ProductList.parse_file(environment.test_products_path)


def test_productlist_to_dataframe(sample_products: ProductList):
    product_df = sample_products.dataframe()

    assert type(product_df) == pd.DataFrame
    assert "title" in product_df.columns
    assert "concatenated_tags" in product_df.columns
    assert product_df.shape == (len(sample_products.products), 2)


def test_categorize(sample_products: ProductList):
    response = client.post("/v1/categorize", json=sample_products.dict())

    # this raises ValidationError if response model is wrong
    predictions = Predictions.parse_obj(response.json())

    assert response.status_code == HTTPStatus.OK
    assert len(predictions.categories) == len(sample_products.products)


@pytest.mark.parametrize(
    "bad_data",
    [
        pytest.param({}, id="Empty data"),
        pytest.param({"products": []}, id="Empty products list"),
        pytest.param(
            {"products": [{"title": "Painel de Festa Baby Shark 5"}]},
            id="Missing Feature",
        ),
        pytest.param(
            {
                "title": "Painel de Festa Baby Shark 5",
                "concatenated_tags": "niver 2 anos baby shark",
            },
            id="Missing Products Key",
        ),
    ],
)
def test_categorize_bad_input(bad_data):
    response = client.post("/v1/categorize", json=bad_data)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
