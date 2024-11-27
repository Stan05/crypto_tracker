# Local Setup

## Start Colima
``colima start``
## Start DB
``docker run --name crypto_tracker -e POSTGRES_PASSWORD=root -e POSTGRES_USER=postgres -e POSTGRES_DB=crypto_tracker -p 5432:5432 -d postgres``

## Create venv 
``python3 -m venv .venv``

## Activate venv
``source .venv/bin/activate``

## Usage
`poetry run python -m crypto_tracker <<command>>`
The list of commands are
 - update_trades - Legacy
 - update_current_prices - Legacy
 - calculate_pnl - Legacy
 - mac_numbers_price_sync - Legacy
 - add_wallet

## Scheduled Jobs
1. Run ``poetry run python -m crypto_tracker.schedulers.update_current_prices``

## DB Migrations

1. Change the ORM files
2. Run `poetry run alembic revision --autogenerate -m "<message>"` to generate the migration file
3. Run `poetry run alembic upgrade head` to execute the migration