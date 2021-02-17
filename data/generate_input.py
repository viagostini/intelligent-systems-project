import json

import pandas as pd

df = pd.read_csv("data/test_products.csv", usecols=["title", "concatenated_tags"])

input_dict = {"products": df.to_dict(orient="records")}


with open("data/test_products.json", "w") as test_file:
    json.dump(input_dict, test_file, ensure_ascii=False)
