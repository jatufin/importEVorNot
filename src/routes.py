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
SCHEMA_FILE = "nettiauto/feature_names.json"
MODEL_FILE = "nettiauto/model.json"
EXAMPLE_X_FILE = "nettiauto/example_X.json"
EXAMPLE_Y_FILE = "nettiauto/example_y.json"

columnns = ['totalOwners', 'kilometers', 'seats', 'power', 'batteryCapacity', 'age', 'isSuv', 'metallicColor', 'airconditioning', 'parking_sensors', 'satellite_navigator', 'cruise_control_adaptive', 'parking_camera_simple_camera', 'seat_heaters', 'driving_assistant', 'alloy_wheels', 'electric_mirrors', 'lane_departure_warning_system', 'electrically_operated_tailgate', 'leather_upholstery', 'emergency_brake_assist', 'collision_avoidance_system', 'cruise_control_traditional', 'parking_assistant', 'tow_bar', 'electric_seats_with_memory', 'heated_steering_wheel', 'sunroof', 'sun_hatch_with_panorama', 'adaptive_headlights', 'sport_seats', 'fuel_battery_powered_heater', 'parking_camera_360-degree_camera', 'battery_preheating', 'electric_seats_without_memory', 'air_suspension', 'curve_lights', 'head_up_display', 'sport_base', 'make_audi', 'make_bmw', 'make_byd', 'make_citroen', 'make_cupra', 'make_dacia', 'make_ds', 'make_fiat', 'make_ford', 'make_hyundai', 'make_jaguar', 'make_kia', 'make_lexus', 'make_maxus', 'make_mazda', 'make_mercedes-benz', 'make_mg', 'make_mini', 'make_muu merkki', 'make_nissan', 'make_opel', 'make_peugeot', 'make_polestar', 'make_porsche', 'make_renault', 'make_seat', 'make_skoda', 'make_subaru', 'make_tesla', 'make_toyota', 'make_volkswagen', 'make_volvo', 'model_2', 'model_208', 'model_3', 'model_500e', 'model_ariya', 'model_atto3', 'model_born', 'model_bz4x', 'model_c4', 'model_c40', 'model_citigo', 'model_combo-e', 'model_cooper', 'model_corsa-e', 'model_e-2008', 'model_e-208', 'model_e-308', 'model_e-berlingo', 'model_e-c4', 'model_e-c4 x', 'model_e-niro', 'model_e-soul', 'model_e-spacetourer', 'model_e-traveller', 'model_e-tron', 'model_e-tron gt', 'model_e-tron gt rs', 'model_e-up!', 'model_enyaq', 'model_eqa', 'model_eqb', 'model_eqc', 'model_eqe', 'model_eqs', 'model_eqs suv', 'model_eqv', 'model_euniq', 'model_ev6', 'model_ev9', 'model_han', 'model_i-pace', 'model_i3', 'model_i3s', 'model_i4', 'model_i4 m50', 'model_i7', 'model_id. buzz', 'model_id3', 'model_id4', 'model_id5', 'model_ioniq 5', 'model_ioniq 6', 'model_ioniq electric', 'model_ix', 'model_ix m60', 'model_ix1', 'model_ix3', 'model_kona', 'model_kona electric', 'model_leaf', 'model_marvel r', 'model_megane', 'model_mg4', 'model_mg5', 'model_mifa 9', 'model_mii electric', 'model_model 3', 'model_model s', 'model_model x', 'model_model y', 'model_mokka', 'model_mokka-e', 'model_mustang', 'model_mustang mach-e', 'model_muu malli', 'model_mx-30', 'model_niro', 'model_proace city verso ev', 'model_proace verso ev', 'model_q4 e-tron', 'model_q8 e-tron', 'model_solterra', 'model_spring', 'model_t90', 'model_tang', 'model_taycan', 'model_twingo', 'model_up!', 'model_ux', 'model_xc40', 'model_zafira-e', 'model_zoe', 'model_zs', 'color_beige', 'color_black', 'color_blue', 'color_brown', 'color_copper', 'color_gray', 'color_green', 'color_orange', 'color_other', 'color_red', 'color_silver', 'color_turquoise', 'color_violet', 'color_white', 'color_yellow', 'driveType_4wd', 'driveType_fwd', 'driveType_rwd']

data_columns = [
  'make',
  'model',
  'color',
  'driveType',
  'totalOwners',
  'kilometers',
  'seats',
  'power',
  'batteryCapacity',
  'age',
  'isSuv',
  'metallicColor',
  'airconditioning',
  'cruise_control_adaptive',
  'satellite_navigator',
  'parking_camera_simple_camera',
  'seat_heaters',
  'alloy_wheels',
  'electric_mirrors',
  'lane_departure_warning_system',
  'electrically_operated_tailgate',
  'emergency_brake_assist',
  'collision_avoidance_system',
  'cruise_control_traditional',
  'parking_assistant',
  'tow_bar',
  'heated_steering_wheel',
  'sunroof',
  'sun_hatch_with_panorama',
  'adaptive_headlights',
  'sport_seats',
  'fuel_battery_powered_heater',
  'parking_camera_360-degree_camera',
  'battery_preheating',
  'electric_seats_without_memory',
  'air_suspension',
  'curve_lights',
  'head_up_display',
  'sport_base'
]

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
    try:
        json_data = json.loads(request.data)
        url = json_data["url"]
        
        id = re.findall(MOBILE_DE_ID_REGEX,  url)[0]
        
        html = request_car_detail_page(id)
        car_data = extract_car_data(html)
    
        return json.dumps(car_data)
    except:
        return "Error occurred when fetching data", 400


# Should get an feature vector and returns a predicted price
@app.route("/predict", methods=["POST"])
def predict():
    try:
        json_data = json.loads(request.data)
        df = pd.DataFrame([json_data])
        df = df[data_columns]
        df_encoded = pd.get_dummies(df, columns=[
            "make",
            "model",
            "color",
            "driveType"
        ])
    
        X = pd.DataFrame(columns=columnns, data=df_encoded)    
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
    except:
        return "Prediction error", 400
    
    
    



