import json

from locust import HttpUser, between, task

API_ROOT = "http://localhost:5000"


class Getter(HttpUser):
    """This user performs predictions on the same payload"""

    host = API_ROOT
    shortlink = ""
    wait_time = between(0.005, 0.01)

    def on_start(self):
        with open("data/test_products.json", "r") as json_file:
            self.data = json.load(json_file)

    @task
    def get_url(self):
        self.client.post("/v1/categorize", json=self.data)
