#!/usr/bin/python3

import pandas as pd
import json
import os
from glob import glob

INPUT_DIR = "query_results"

OUTPUT_FILE_NAME = "results.csv"
OUTPUT_CSV_DELIMITER = ";"

SELECTED_COLUMNS = [
    "id",
    "vehicleType",
    "make",
    "model",
    "modelType",
    "color",
    "colorType",
    "driveType",
    "accessories",
    "price",
    "totalOwners",
    "kilometers",
    "seats",
    "doors",
    "power",
    "batteryCapacity",
    "batteryGuaranteeMonth",
    "batteryGuaranteeKm",
    "electricRange",
    "chargingType",
    "chargingPower",
    "maximumChargingPower"
]

# Read JSON files into single datframe
files = glob(os.path.join(INPUT_DIR, "*.json"))
df = pd.concat((pd.read_json(f) for f in files))
rows, cols = df.shape
print(f"Number of rows imported: {rows} (columns: {cols})")

# Drop columns we are not interested in
df = df[SELECTED_COLUMNS]

# Replace dictionary values with a field value in the dictionary
def dictReplacer(a):
    # Replace a list of dictionaries with comma separated values
    if isinstance(a, list):
        for i, item in enumerate(a):
            a[i] = dictReplacer(item)
        return ",".join(a)

    if not isinstance(a, dict):
        return a

    # Most dictionary values have fields: id, en, fi
    if "en" in a:
        return a["en"]

    # Make and model column contain a dict with a field: name
    if "name" in a:
        return a["name"]

    return a

df = df.map(dictReplacer, na_action="ignore")

# Save the dataframe
df.to_csv(OUTPUT_FILE_NAME, index=False)

print(f"File '{OUTPUT_FILE_NAME}' created")
