## Tax Calculator
Simple Django app with single endpoint for calculating income tax.

### Starting the project
1. Clone repository `git clone git@github.com:zyks/tax-calc.git`
2. Run `cp .env_sample .env` to create `.env` file in root folder
3. Run `docker-compose up` to build images and start containers
4. Run `docker-compose exec backend python manage.py load_tax_bands` to populate database with tax rates data from
`tax_bands.json`.
5. Send POST request to `/api/calculator/tax/` endpoint to calculate tax, set `country` (`UK` / `PL`) and `income`
body parameters.
6. Run `docker-compose exec backend python3 manage.py test` to start tests.


### Example request
```shell script
> curl -X POST -H "Content-Type: application/json"  -d '{"income": 52000, "country": "UK"}' localhost:8000/api/calculator/tax/

{"tax": 8300.0}
```
```shell script
>  curl -X POST -H "Content-Type: application/json"  -d '{"income": 157300, "country": "PL"}' localhost:8000/api/calculator/tax/

{"tax" 37506.8}
```
Set `detailed` boolean parameter to `true` to see detailed calculation results.
```shell script
> curl -X POST -H "Content-Type: application/json"  -d '{"income": 235570, "country": "UK", "detailed": true}' localhost:8000/api/calculator/tax/

{
    "tax": 86006.5,
    "details": [
        {
            "income_from": 150000,
            "income_to": None,
            "tax_rate": 0.45,
            "tax": 38506.5
        },
        {
            "income_from": 50000,
            "income_to": 150000,
            "tax_rate": 0.4,
            "tax": 40000.0
        },
        {
            "income_from": 12500,
            "income_to": 50000,
            "tax_rate": 0.2,
            "tax": 7500.0
        },
        {
            "income_from": 0,
            "income_to": 12500,
            "tax_rate": 0.0,
            "tax": 0.0
        }
    ]
}
```
