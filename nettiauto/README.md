# Nettiauto dataset

after new data has been acquired from the provider, these preprocessing steps should be performed before running the server. This must be done only once after a dataset have been obtained.

For the dataset already loaded in the repository this has already been done, and performing these actions are not needed.


## Query data from the service

These steps are required only if one wants to update the dataset. A full dataset have already been downloaded in the `query_results` folder. Registration is needed for running the queries the process can require considerable amount of handwork and time.

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

## Processing downloaded JSON files and training the model

1. Download json files to the *query_results* directory (not mandatory, since there is a full dataset already queried)
1. Run the Jupyter notebook `nettiauto_dataset_parsing.ipynb`to preprocess the data and create dataset file
1. Run the Jupyter notebook `nettiauto_model.ipynb` to train and create the model file from the preprocessed datase
1. The resulting files will be used by the server

### Running Jupyter in Poetry

To avoid dependency issues, Jupyter can be run from inside the Poetry environment:

```
poetry run jupyter notebook nettiauto_dataset_parsing.ipynb
poetry run jupyter notebook nettiauto_model.ipynb
```

