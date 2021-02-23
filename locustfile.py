import json
from random import randint, sample

from locust import HttpUser, between, task

API_ROOT = "http://localhost:5000"


class User(HttpUser):
    """
    This user performs predictions on a randomized payload with the number of elements
    in the request following a normal distribution with mean 100 and standard deviation
    of 20. The data itself is a single product repeated many times.
    """

    host = API_ROOT
    wait_time = between(0.005, 0.01)

    def on_start(self):
        with open("data/test_products.json", "r") as json_file:
            raw_data = json.load(json_file)["products"]
            self.data = {"products": sample(raw_data, 1) * randint(1, 1000)}

    @task
    def get_url(self):
        self.client.post("/v1/categorize", json=self.data)
