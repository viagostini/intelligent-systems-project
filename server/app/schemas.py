"""Definition of request and response schemas.

This module defines all schemas using Pydantic, which allows for automatic field
validation and json (de)serialization when used with FastAPI routes.

Using these schemas with FastAPI also allows for auto generated docs to display
information about them in the `/docs` route.
"""

from typing import List

import pandas as pd
from pydantic import BaseModel


class Product(BaseModel):
    title: str
    concatenated_tags: str


class ProductList(BaseModel):
    products: List[Product]

    def dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.dict()["products"])


class Predictions(BaseModel):
    categories: List[str]
