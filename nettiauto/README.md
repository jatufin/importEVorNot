## Processing downloaded JSON files

1. Download json files to the *query_results* directory
1. Run `./preprocess.py`
1. Results will be saved to the *preprocessed_results.csv* file

## Query data from the service

1. Sign-in to Nettauto
1. Copy a cookie string: `nettix-token-user`
1. Open in a browser: `api.nettix.fi/docs/car/`
1. Open Authorize
1. Paste the cookie string to X-Access-Token
1. Click Authorize
1. Click Close
1. Run desired requests from the page

### Some useful fields in the query and result data

1. page: search result page number
1. rows: 1-100 (results on each page)
1. fuelType: 4 ({id:4,fi:"Sähkö","en":"Electric"})
1. vehicleType: 1 (Henkilöauto)
1. firstRegistrationMonth
1. firstRegistrationYear
1. yearFrom: Minimum year of manufacture
1. yearTo: Maximum year of manufacture
1. bodyType: sedan, SUV, etc. (see separate json)

### Searches made on 30.10.2023:

```
vehicleType: 1, fuelType: 4, yearFrom: 2021, yearTo: 2021
Count: 807
Result pages received (max 100 results per page): 9

vehicleType: 1, fuelType: 4, yearFrom: 2022, yearTo: 2022
Count: 1306
Result pages received (max 100 results per page): 14

vehicleType: 1, fuelType: 4, yearFrom: 2023, yearTo: 2023
Count: 2021
Result pages received (max 100 results per page): 21

vehicleType: 1, fuelType: 4, yearFrom: 2024, yearTo: 2024
Count: 91
Result pages received (max 100 results per page): 1
```

## Processing columns and filling missing data

* id: no change
* vehicleType: Mode of the same make and model
* make: discard row if missing
* model: Mode of the same make
* modelType: Mode of the same model
* color: mode
* colorType: mode
* driveType: mode of the same model
* accessories: Extract to boolean (0 or 1) columns
* price: Median of the same model/year
* totalOwners: Median
* kilometers: Median of the year
* seats: Mode of the same model/year
* doors: Mode of the same model/year
* power: Mean of the same model/year
* batteryCapacity: Mode of the same model/year
* batteryGuaranteeMonth: no change
* batteryGuaranteeKm: no change
* electricRange: Mean of the same model/year
* chargingType: no change
* chargingPower: no change
* maximumChargingPower: no change

