import json
import unittest
from http import HTTPStatus

from api import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_categorize(self):
        data = {
            "products": [
                {
                    "title": "Painel de Festa Baby Shark 5",
                    "concatenated_tags": "niver 2 anos baby shark",
                }
            ]
        }
        response = self.client.post("/v1/categorize", json=data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_categorize_404(self):
        data = {
            "products": [
                {
                    "title": "Painel de Festa Baby Shark 5",
                }
            ]
        }
        response = self.client.post("/v1/categorize", json=data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)