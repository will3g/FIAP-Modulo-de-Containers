import sys

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    msg = ''
    if len(sys.argv) > 1: msg = f' from {sys.argv[1]}'
    return f'Hello, Docker{msg}!'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
