import requests
from flask import Flask
from random import randint
app = Flask(__name__)


def generate_keys(lenght):
    caracteres = "qwertyuipoasdfghjklzxcvbnm1234567890-_+*!/"
    key = ''
    while len(key) < lenght:
        value = caracteres[randint(0, 41)]
        if randint(0, 1) == 1:
            value = value.upper()
        key = key + value
    return key


def build_token():
    return generate_keys(37) + '.' + generate_keys(72) + '.' + generate_keys(42)


@app.route('/url-ataques')
def attack():
    headers = {"Authorization": "Bearer " + build_token()}
    print("REQUEST :" + headers)
    return requests.get('http://localhost:5000/pacientes', headers).content