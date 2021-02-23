import json

import cloudpickle
from fastapi import FastAPI, Response

from app.monitoring import instrumentator
from app.schemas import Environment, Predictions, ProductList

env = Environment()

app = FastAPI()

# enables instrumentation for Prometheus
instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)


with open(env.model_path, "rb") as model_file:
    model = cloudpickle.load(model_file)


@app.post("/v1/categorize", response_model=Predictions)
def categorize(response: Response, products: ProductList):
    products_df = products.dataframe()
    predictions = {"categories": list(model.predict(products_df))}
    response.headers["X-predictions"] = json.dumps(predictions)
    return predictions
