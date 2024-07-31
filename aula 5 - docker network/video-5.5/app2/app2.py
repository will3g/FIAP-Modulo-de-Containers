import os

from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

APP_HOST = os.getenv('APP_HOST')
APP_PORT = int(os.getenv('APP_PORT'))

MONGODB_PASS = os.getenv('MONGODB_PASS')
MONGODB_USER = os.getenv('MONGODB_USER')
MONGODB_PORT = os.getenv('MONGODB_PORT')
MONGODB_HOSTNAME = os.getenv('MONGODB_HOSTNAME')
MONGODB_DATABASE = str(os.getenv('MONGODB_DATABASE'))
MONGODB_COLLECTION = str(os.getenv('MONGODB_COLLECTION'))

MONGODB_URI = f'mongodb://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_HOSTNAME}:{MONGODB_PORT}/'



@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 'ok'})

@app.route('/ticker/<string:ticker>', methods=['GET'])
def get_ticker_data(ticker):
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DATABASE]
    collection = db[MONGODB_COLLECTION]

    record = collection.find_one({'ticker': ticker.upper()})
    if record:
        return jsonify(record['data'])
    else:
        return jsonify({'error': 'Ticker not found'}), 404
    client.close()


if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT)
