from typing import List

import pandas as pd
from pydantic import BaseModel


class Product(BaseModel):
    title: str
    concatenated_tags: str


class ProductList(BaseModel):
    products: List[Product]

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.dict()["products"])


class Predictions(BaseModel):
    categories: List[str]
