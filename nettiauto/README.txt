How to acquire data files from the service:

- Sign-in to Nettauto
- Copy a cookie string: nettix-token-user
- Open https://api.nettix.fi/docs/car/
- Open Authorize
- Paste the cookie string to X-Access-Token
- Click Authorize
- Click Close
- Run desired requests from the page

Some useful fields:
page: search result page number
rows: 1-100 (results on each page)
fuelType: 4 ({id:4,fi:"Sähkö","en":"Electric"})
vehicleType: 1 (Henkilöauto)
firstRegistrationMonth
firstRegistrationYear
yearFrom: Minimum year of manufacture
yearTo: Maximum year of manufacture
bodyType: sedan, SUV, etc. (see separate json)

Searches made on 30.10.2023:

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


