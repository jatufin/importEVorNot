from app import app
from flask import redirect, render_template, request, Response

import json
import pandas as pd
import  xgboost as xgb
import re

from mobilede_utils import request_car_detail_page
from mobilede_parser import extract_car_data

MOBILE_DE_ID_REGEX = r'id=(\d+)&'

MODEL_ABSOLUTE_MEAN_ERROR = 3200

# The files are generated with a Jupyter notebook:
#  nettiauto/nettiauto_model.ipynb
DATA_COLUMN_FILE = "nettiauto/data_columns.txt"
MODEL_FILE = "nettiauto/model.json"

with open(DATA_COLUMN_FILE,"r") as f:
    data_columns = [line.rstrip() for line in f]

xgb_regressor = xgb.XGBRegressor()
xgb_regressor.load_model(MODEL_FILE)

@app.route("/schema", methods=["GET"])
def schema():
    return json.dumps(features)

# Should get an URL and return a vehicle vector
# as Pandas dataframe JSON dump
# Example can be found in file: nettiauto/example_X.json
@app.route("/fetch", methods=["POST"])
def fetch():
    try:
        json_data = json.loads(request.data)
        url = json_data["url"]

        id = re.findall(MOBILE_DE_ID_REGEX,  url)[0]

        html = request_car_detail_page(id)

        print("EXTRACT CAR DATA")        
        car_data = extract_car_data(html)

        img_url_regex =r'<meta property=\"og:image:url\" content=\"(https:\/\/.*.jpg)\"\/><meta property=\"og:image:type\" content=\"image\/jpeg\"\/>'
        car_data["img_url"] = re.findall(img_url_regex, html)[0]
        
        return json.dumps(car_data)
    except Exception as e:
        return f"Error occurred when fetching data: {e}", 400


# Should get an feature vector and returns the predicted price
@app.route("/predict", methods=["POST"])
def predict():
    try:
        json_data = json.loads(request.data)
        df = pd.json_normalize(json_data["query"])
        df = df[data_columns]
        df_encoded = pd.get_dummies(df, columns=[
            "make",
            "model",
            "color",
            "driveType"
        ])

        columns = xgb_regressor.get_booster().feature_names
        X = pd.DataFrame(columns=columns, data=df_encoded)
        
        predicted = xgb_regressor.predict(X)    
        
        prediction_f = float(predicted[0])
        
        return json.dumps({
            "prediction": {
                "price": round(prediction_f),
                "low": round(prediction_f - MODEL_ABSOLUTE_MEAN_ERROR),
                "high": round(prediction_f + MODEL_ABSOLUTE_MEAN_ERROR),
            },
            "original_price": round(json_data.get('price', 0)),
            "price_delta": round(prediction_f - json_data.get('price', 0)),
        })
    except Exception as e:
        return f"The prediction could not be produced: {e}", 400
    
    
    



