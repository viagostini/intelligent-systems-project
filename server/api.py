import os
from typing import List

import cloudpickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


MODEL_PATH = os.environ["MODEL_PATH"]
with open(MODEL_PATH, "rb") as model_file:
    model = cloudpickle.load(model_file)


class Product(BaseModel):
    title: str
    concatenated_tags: str


class ProductList(BaseModel):
    products: List[Product]

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.dict()["products"])


class Predictions(BaseModel):
    categories: List[str]


@app.post("/v1/categorize", response_model=Predictions)
async def categorize(products: ProductList):
    df = products.to_dataframe()
    predictions = list(model.predict(df))
    return {"categories": predictions}
