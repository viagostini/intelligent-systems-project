import json
import os
from http import HTTPStatus

import joblib
import pandas as pd
from flask import Flask, Response, request

app = Flask(__name__)


MODEL_PATH = os.environ["MODEL_PATH"]
model = joblib.load(MODEL_PATH)


@app.route("/v1/categorize", methods=["POST"])
def categorize():
    try:
        df = pd.DataFrame(request.json["products"])
        predictions = model.predict(df)
        predictions_json = {"categories": list(predictions)}
    except:
        return Response(response="Malformed input", status=HTTPStatus.BAD_REQUEST)
    return Response(
        response=json.dumps(predictions_json, ensure_ascii=False),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@app.route("/v1/ping")
def ping():
    status = 200 if model is not None else 404
    return Response(response="\n", status=status, mimetype="application/json")
