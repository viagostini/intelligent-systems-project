import pytest
from fastapi.testclient import TestClient

from api import app
from models import Environment, ProductList

env = Environment()
client = TestClient(app)


def test_categorize():
    data = ProductList.parse_file(env.test_products_path)

    response = client.post("/v1/categorize", json=data.dict())

    assert response.status_code == 200
    assert "categories" in response.json()
    assert len(response.json()["categories"]) == len(data.products)


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
