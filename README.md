# API Source ETL Scripts
This is an application for fetching data for different sources such as:
- twitter
- file storage

## Requirements
- Python 3.8 or higher

## Setup (as standalone locally)
1. Install requirements `pip install -r ./app/requirements`
2. Create .env file `cp ./app/.env.example ./app/.env` and use valid values
3. Run application `python ./app/main.py`

## Setup by using Docker-Compose
1. Create .env file `cp ./app/.env.example ./app/.env` and use valid values
2. Start docker by using `docker-compose up`
