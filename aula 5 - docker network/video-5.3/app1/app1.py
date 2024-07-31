import re
import os

import logging
import requests
import pandas as pd
import yfinance as yf

from bs4 import BeautifulSoup
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Não é muito beeem uma api, mas serve para simulação ;)
EXTERNAL_API = os.getenv('EXTERNAL_API')

MONGODB_PASS = os.getenv('MONGODB_PASS')
MONGODB_USER = os.getenv('MONGODB_USER')
MONGODB_PORT = os.getenv('MONGODB_PORT')
MONGODB_HOSTNAME = os.getenv('MONGODB_HOSTNAME')
MONGODB_DATABASE = str(os.getenv('MONGODB_DATABASE'))
MONGODB_COLLECTION = str(os.getenv('MONGODB_COLLECTION'))

MONGODB_URI = f'mongodb://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_HOSTNAME}:{MONGODB_PORT}/'


def get_tickers():
    logger.info(f'[INFO] GETTING DATA FROM {EXTERNAL_API}')
    response = requests.get(EXTERNAL_API)
    soup = BeautifulSoup(response.text, 'html.parser')
    logger.info('CREATING LIST OF TICKERS...')
    tickers = []
    for ticker_tag in soup.find_all('a'):
        if '"/acoes/' in str(ticker_tag): tickers.append(f'{ticker_tag.text}.SA')
    logger.info(f'[INFO] TOTAL TICKERS {len(tickers)}')
    return tickers

def update_database():
    logger.info('CREATING CONNECTION...')
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]
    logger.info('COLLECTION CREATED WITH SUCCESS!...')
    
    logger.info('GETTING TICKERS!...')
    tickers = get_tickers()

    for ticker in tickers:
        logger.info(f'[INFO] INSERTING DATA OF TICKER: {ticker}...')
        existing_record = collection.find_one({'ticker': ticker})
        if existing_record:
            last_date = pd.to_datetime(existing_record['data'][-1]['Date'])
            data = yf.Ticker(ticker).history(start=last_date + pd.Timedelta(days=1))
            if not data.empty:
                data.reset_index(inplace=True)
                new_records = data.to_dict('records')
                collection.update_one({'ticker': ticker}, {'$push': {'data': {'$each': new_records}}})
        else:
            data = yf.Ticker(ticker).history(start='2020-01-01', end='2024-07-31')
            data.reset_index(inplace=True)
            records = data.to_dict('records')
            collection.insert_one({'ticker': ticker.replace('.SA', ''), 'data': records})

    client.close()

scheduler = BlockingScheduler()
# função de dados é agendada para executar após 24h
scheduler.add_job(update_database, 'interval', days=1)
scheduler.start()


if __name__ == "__main__":
    update_database()