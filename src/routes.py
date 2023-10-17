from app import app
from flask import redirect, render_template, request

import json
import pandas as pd
import  xgboost as xgb

# The files are generated with a Jupyter notebook:
#  nettiauto/nettiauto_model.ipynb
SCHEMA_FILE = "nettiauto/feature_names.json"
MODEL_FILE = "nettiauto/model.json"
EXAMPLE_X_FILE = "nettiauto/example_X.json"
EXAMPLE_Y_FILE = "nettiauto/example_y.json"

with open(SCHEMA_FILE,"r") as f:
    features = json.load(f)

xgb_regressor = xgb.XGBRegressor()
xgb_regressor.load_model(MODEL_FILE)

# TODO: Remove test vector, when not needed
with open(EXAMPLE_X_FILE,"r") as f:
    example_X = json.load(f)
with open(EXAMPLE_Y_FILE,"r") as f:
    example_y = json.load(f)


@app.route("/schema", methods=["GET"])
def schema():
    return json.dumps(features)

# TODO: This is only a mock
# Should get an URL and return a vehicle vector
# as jsond fump of a Pandas dataframe
# Example in file: nettiauto/example_X.json
@app.route("/fetch", methods=["POST"])
def fetch():
    json_data = json.loads(request.data)
    url = json_data["url"]

    # TODO: implement
    # X = fecth_from_mobile(url)
    X = example_X # mock
    
    return json.dumps(X)

# Should get an feature vector and returns a predicted price
@app.route("/predict", methods=["POST"])
def predict():
    json_data = json.loads(request.data)
    query_json_string = json_data["query"]

    X = pd.read_json(query_json_string, orient="split")
    
    predicted = xgb_regressor.predict(X)    

    return json.dumps({ "price": str(predicted[0]) })
    
    
    



