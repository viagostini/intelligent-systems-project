import json

import cloudpickle
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from models import Environment, Predictions, ProductList
from monitoring import instrumentator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# enables instrumentation for Prometheus
instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)


env = Environment()


with open(env.model_path, "rb") as model_file:
    model = cloudpickle.load(model_file)


@app.post("/v1/categorize", response_model=Predictions)
async def categorize(response: Response, products: ProductList):
    products_df = products.to_dataframe()
    predictions = {"categories": list(model.predict(products_df))}
    response.headers["X-predictions"] = json.dumps(predictions)
    return predictions
