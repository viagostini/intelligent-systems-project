import json

import pandas as pd

with open("data/test_products.json", "r") as test_file:
    df_json = json.load(test_file)


df = pd.DataFrame(df_json["products"])