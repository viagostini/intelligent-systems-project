import pandas as pd
import pytest
from fastapi.testclient import TestClient

from api import app
from models import Environment, ProductList

env = Environment()
client = TestClient(app)


@pytest.fixture
def sample_products():
    return ProductList.parse_file(env.test_products_path)


def test_productlist_to_dataframe(sample_products: ProductList):
    product_df = sample_products.dataframe()

    assert type(product_df) == pd.DataFrame
    assert "title" in product_df.columns
    assert "concatenated_tags" in product_df.columns
    assert product_df.shape == (len(sample_products.products), 2)


def test_categorize(sample_products: ProductList):
    response = client.post("/v1/categorize", json=sample_products.dict())

    assert response.status_code == 200
    assert "categories" in response.json()
    assert len(response.json()["categories"]) == len(sample_products.products)


@pytest.mark.parametrize(
    "bad_data",
    [
        pytest.param({}, id="Empty data"),
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

    assert response.status_code == 422
