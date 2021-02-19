import json
import os

import cloudpickle
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from models import Predictions, ProductList
from monitoring import instrumentator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

instrumentator.instrument(app).expose(app, include_in_schema=False, should_gzip=True)

if os.environ.get("COMPOSE_PROJECT_NAME") is None:
    load_dotenv(".env.local")

MODEL_PATH = os.environ["MODEL_PATH"]
with open(MODEL_PATH, "rb") as model_file:
    model = cloudpickle.load(model_file)


@app.post("/v1/categorize", response_model=Predictions)
async def categorize(response: Response, products: ProductList):
    df = products.to_dataframe()
    predictions = {"categories": list(model.predict(df))}
    response.headers["X-predictions"] = json.dumps(predictions)
    return predictions
