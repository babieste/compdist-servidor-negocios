from flask import Flask, abort
from dotenv import load_dotenv
from os import environ
import requests

load_dotenv()

servidor_dados_url = environ.get('SERVIDOR_DADOS_URL')

app = Flask(__name__)

tokens = [
    {'serv_negocio_id': 1, 'auth_token': 'secret#1'},
    {'serv_negocio_id': 2, 'auth_token': 'secret#2'},
    {'serv_negocio_id': 3, 'auth_token': 'secret#3'},
]

def get_auth_token(id):
    auth_token = None
    for token in tokens:
        if token['serv_negocio_id'] == id:
            auth_token = token['auth_token']  
    return auth_token

@app.route("/")
def index():
    return 'Hello World!'

# Aumenta o saldo da conta <conta_id> pelo valor <valor> e retorna nada
@app.put('/deposito/<conta_id>/<valor>')
def deposito(conta_id, valor):
    return {
        'operation': 'deposito',
        'conta_id': conta_id,
        'valor': valor
    }

# Diminui o saldo da conta <conta_id> pelo valor <valor> e retorna nada
@app.put('/saque/<conta_id>/<valor>')
def saque(conta_id, valor):
    return {
        'operation': 'saque',
        'conta_id': conta_id,
        'valor': valor
    }

# Retorna o saldo da conta <conta_id>
@app.get('/saldo/<conta_id>')
def saldo(conta_id):

    auth_token = get_auth_token(str(conta_id))
    print(auth_token)
    if auth_token != None:
        response = requests.get(
            'http://' + servidor_dados_url + '/conta/' + conta_id + '/saldo',
            headers={'authorization': auth_token}
        )

        converted_response = response.json()
        return converted_response
    abort(app.make_response(
        ({'message': 'Not Authorized'}, 401)
    ))

# Transferência da conta <conta_origem> para a conta <conta_dest> do valor <valor>
@app.put('/transferencia/<conta_origem>/<conta_dest>/<valor>')
def transferencia(conta_origem, conta_dest, valor):
    return {
        'operation': 'transferencia',
        'conta_origem': conta_origem,
        'conta_dest': conta_dest,
        'valor': valor
    }

