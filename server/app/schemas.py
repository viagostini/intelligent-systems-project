import os
from typing import List

import pandas as pd
from dotenv import load_dotenv
from pydantic import BaseModel, BaseSettings

if os.environ.get("COMPOSE_PROJECT_NAME") is None:
    load_dotenv(".env.local")


class Environment(BaseSettings):
    model_path: str
    test_products_path: str


class Product(BaseModel):
    title: str
    concatenated_tags: str


class ProductList(BaseModel):
    products: List[Product]

    def dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.dict()["products"])


class Predictions(BaseModel):
    categories: List[str]
