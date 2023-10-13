from app import app

from flask import redirect, render_template, request

import json

SCHEMA_FILE = "nettiauto/feature_names.json"
MODEL_FILE = "nettiauto/model.json"
EXAMPLE_X_FILE = "nettiauto/example_X.json"
EXAMPLE_Y_FILE = "nettiauto/example_y.json"

with open(SCHEMA_FILE,"r") as f:
    features = json.load(f)

with open(MODEL_FILE,"r") as f:
    model = json.load(f)

with open(EXAMPLE_X_FILE,"r") as f:
    example_X = json.load(f)

with open(EXAMPLE_Y_FILE,"r") as f:
    example_y = json.load(f)

# TODO: To be removed
@app.route("/")
def main():
    return redirect("/index")

# TODO: To be removed
@app.route("/index")
def index():
     return render_template("index.html", foo="Bar")

@app.route("/schema", methods=["GET"])
def schema():
    return json.dumps(features)

# TODO: This is only a mock
# Should get an URL and return a vehicle vector
@app.route("/fetch", methods=["POST"])
def fetch():
    print(f"POST REQUEST /fetch DATA: {request.data}")
    
    return json.dumps(example_X)

# TODO: This is only a mock
# Should get an feature vector and return a predicted price
@app.route("/predict", methods=["POST"])
def predict():
    print(f"POST REQUEST /predict DATA: {request.data}")
    
    return json.dumps(example_y)



