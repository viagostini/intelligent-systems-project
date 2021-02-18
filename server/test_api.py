import json

import pytest
from api import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_categorize():
    with open("/usr/src/data/test_products.json", "r") as json_file:
        data = json.load(json_file)

    response = client.post("/v1/categorize", json=data)

    assert response.status_code == 200
    assert "categories" in response.json()
    assert len(response.json()["categories"]) == len(data["products"])


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
