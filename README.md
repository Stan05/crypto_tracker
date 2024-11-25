### Local Setup

#### Start Colima
``colima start``
#### Start DB
``docker run --name crypto_tracker -e POSTGRES_PASSWORD=root -e POSTGRES_USER=postgres -e POSTGRES_DB=crypto_tracker -p 5432:5432 -d postgres``

#### Create venv 
``python3 -m venv .venv``

#### Activate venv
``source .venv/bin/activate``

### Usage
`poetry run python -m crypto_tracker <<command>>`
The list of commands are
 - update_trades 
 - update_current_prices
 - calculate_pnl
 - mac_numbers_price_sync

## Scheduled Jobs

### Run
``poetry run python -m crypto_tracker.schedulers.update_current_prices``