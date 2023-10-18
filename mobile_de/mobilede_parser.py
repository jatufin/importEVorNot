from bs4 import BeautifulSoup
import unicodedata
import re

import pandas as pd


CURRENT_YEAR = 2023
CURRENT_MONTH = 10

# TODO paths not working now in notebook.
drivetype_df = pd.read_csv('./mobile_de/drivetype.csv')
capacities = pd.read_csv('./mobile_de/capacities.csv')
nettiauto_data = pd.read_csv("./nettiauto/nettiauto_dataset.csv")
make_model_mean_capacities = nettiauto_data.groupby(by=["make","model"])["batteryCapacity"].mean()

def get_capacity(make, model, modelTypeName):
    m = (capacities["make"] == make) & (capacities["model"] == model)
    for i, row in capacities[m].iterrows():
        if bool(re.search(r'{}'.format(row["regex"]), modelTypeName, re.I)) ^ bool(row["inverse"]):
            return float(row["batteryCapacity"])
    if (make, model) in make_model_mean_capacities.index:
        return float(make_model_mean_capacities[make, model])
    raise Exception("Battery capacity missing and it cannot be deduced with given model.")

def get_age(reg_y, reg_m):
    if reg_y and reg_m:
        return CURRENT_YEAR - reg_y + (CURRENT_MONTH - reg_m) / 12
        
    return CURRENT_YEAR - reg_y

def get_drive_type(make, model, features):
    if 'Four wheel drive' in features:
        return '4wd'
    make_df = drivetype_df[(drivetype_df['make'] == make) &( drivetype_df['model'] == model)].sort_values(by='driveType', ascending=False).reset_index(drop=True)
    return make_df['driveType'].iloc[0]


FEATURES_TO_COLUMN_NAME = {
    'Adaptive Cruise Control': 'parking_sensors',
    'Navigation system': 'satellite_navigator',
    'Adaptive Cruise Control': 'cruise_control_adaptive',
    'Parking sensor: Camera': 'parking_camera_simple_camera',
    'Heated seats': 'seat_heaters',
    'Alloy wheels': 'alloy_wheels',
    'Electric side mirror': 'electric_mirrors',
    'Lane change assist': 'lane_departure_warning_system',
    'Electric tailgate': 'electrically_operated_tailgate',
    'Emergency brake assist': 'emergency_brake_assist',
    'Collision avoidance system': 'collision_avoidance_system',
    'Cruise control: Traditional': 'cruise_control_traditional',
    'Parking sensor: Self-steering systems': 'parking_assistant',
    'Trailer coupling, swiveling': 'tow_bar', # done
    'Trailer coupling, detachable': 'tow_bar', # done
    'Trailer coupling, fix': 'tow_bar', # done
    'Heated steering wheel': 'heated_steering_wheel', # done
    'Sunroof': 'sunroof', # done
    'Panoramic roof': 'sun_hatch_with_panorama', # done
    'Adaptive lighting': 'adaptive_headlights', # done
    'Sport seats': 'sport_seats', # done
    'Auxiliary heating': 'fuel_battery_powered_heater', # done
    'Parking sensor: 360° camera': 'parking_camera_360-degree_camera', # muutetaan kameraksi vain
    'Battery preheating': 'battery_preheating',
    'Electric seat adjustment': 'electric_seats_without_memory', # check
    'Air suspension': 'air_suspension', # done
    'Adaptive cornering lights': 'curve_lights', # done
    'Head-up display': 'head_up_display', # done
    'Sports suspension': 'sport_base', # done,    
}


def _parse_number(string):
    """Parse e.g. 43.400 € to 43400 or 12.500 km to 12500"""
    return ("").join(re.findall(r"\d+", string))

def _parse_capacity(s):
    return re.findall("(\d{2,3})\s*kWh", s.get_text(), re.I) if s else []

def _get_capacity(soup):
    res = _parse_capacity(soup.find(id="batteryCapacity-v"))
    if (res == []):
        res = _parse_capacity(soup.find("div", {"class": "listing-title"}).find("div", {"class": "listing-subtitle"}))
    if (res == []):
        res = _parse_capacity(soup.find("div", {"class", "g-col-12 description"}))
    if len(res):
        return sorted(res, reverse=True)[0]
    return None

def extract_car_data(html):
    page_n = unicodedata.normalize("NFKD", html)
    soup = BeautifulSoup(page_n, 'html.parser')
    first_registration_elements = soup.find_all(class_='key-feature key-feature--firstRegistration')
    if not len(first_registration_elements):
        raise 'Not a used car'

    first_registration_element = first_registration_elements[0]
    first_registration_text = first_registration_element.find('div', class_='key-feature__value').text.strip()
    first_registration_parts = first_registration_text.split('/')
    firstRegistrationMonth = int(first_registration_parts[0])
    firstRegistrationYear = int(first_registration_parts[1])

    data = {
        'firstRegistrationMonth': firstRegistrationMonth,
        'firstRegistrationYear': firstRegistrationYear,
    }
    data["make"], data["model"] = soup.find(id="ad-title").get_text().split(" ", 1)
    data["modelTypeName"] = soup.find_all(class_='listing-subtitle')[0].get_text()
    data["color"], color_type, *_ = s.get_text().split() + ["Nonmetallic"] if (s:=soup.find(id="color-v")) else [None, None]
    data["metallicColor"] = "Metallic" in color_type
    data["kilometers"] = _parse_number(soup.find(id="mileage-v").get_text())
    data["price"] = _parse_number(soup.find("span", {"data-testid" : "prime-price"}).get_text())
    data["registration"] = s.get_text() if (s:=soup.find(id="firstRegistration-v")) else None
    data["electric"] = soup.find(id="fuel-v").get_text() == "Electric"
    data["power"] = re.findall(r"\d+", soup.find(id="power-v").get_text())[0]
    data["batteryCapacity"] = _get_capacity(soup)
    data["automatic"] = s.get_text() == "Automatic transmission" if (s:=soup.find(id="transmission-v")) else None
    data["undamaged"] = s.get_text() == "Accident-free" if (s := soup.find(id="damageCondition-v")) else None
    data["seats"] = s.get_text() if (s:= soup.find(id="numSeats-v")) else None
    data["leather_upholstery"] = "leather" in s.get_text().lower() if (s:= soup.find(id="interior-v")) else None  
    data["isSUV"] = ("SUV" in s.get_text()) if (s:= soup.find(id="category-v")) else None
    data["airconditioning"] = ("no climatisation" not in s.get_text().lower()) if (s:= soup.find(id="climatisation-v")) else None

    s= soup.find(id="envkv.wltp.powerConsumption-v")
    res = re.findall(r"(\d+,\d+)", s.get_text()) if s else None
    data["elec_cons"] = res[0].replace(",", ".") if res and len(res) else None

    s = soup.find("div", {"class" : "key-feature key-feature--numberOfPreviousOwners"})
    s = s.find("div", {"class" : "key-feature__value"}) if s else None
    data["n_prev_owners"] = s.get_text() if s else None

    data["features"] = [item.get_text() for item in soup.find(id="features").find_all("div", {"class" : "bullet-list"})]
    if (s:= soup.find(id="parkAssists-v")):
        data["features"] = data["features"] + list(map(lambda x: f"Parking sensor: {x.strip()}", s.get_text().split(",")))
        
        
    # jatkuu
    
    make = data.get('make', '').lower()
    model = data.get('model', '').lower().replace('id.', 'id')
    totalOwenrs_string = data['n_prev_owners'] if 'n_prev_owners' in data and data['n_prev_owners'] else 1

    features_set = set(data['features'])

    result = {
        'make': make,
        'model': model,
        'color': data.get('color', '').lower(),
        'driveType': get_drive_type(make, model, data['features']),
        'price': float(data.get('price', '-1')),
        'totalOwners': int(totalOwenrs_string),
        'kilometers': int(data.get('kilometers', '-1')),
        'seats': int(data.get('seats', '5')),
        'power': float(data.get('power', '-1')),
        'batteryCapacity': float(c) if (c:=data['batteryCapacity']) else get_capacity(make, model, data["modelTypeName"]),
        'age': get_age(data['firstRegistrationYear'], data['firstRegistrationMonth']),
        'isSuv': data['isSUV'],
        'metallicColor': data['metallicColor'],
        'airconditioning': data['airconditioning'],
        **{FEATURES_TO_COLUMN_NAME[key]: key in features_set for key in FEATURES_TO_COLUMN_NAME.keys()}
    }
            
    return result

def parse_ad_ids(html):
    return re.findall(r"data-listing-id=(\d+)\s", html)