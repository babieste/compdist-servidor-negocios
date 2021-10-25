from logging import exception
from flask import Flask, abort
from dotenv import load_dotenv
from os import environ
import requests
from requests.api import get

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

def raise_server_error():
    abort(app.make_response(
        ({'message': 'Não foi possível realizar a operação.'}, 500)
    ))

def raise_not_authorized():
    abort(app.make_response(
        ({'message': 'Não autorizado.'}, 401)
    ))

def _saldo(conta_id, auth_token):
    # Retorna saldo
    saldo_response = requests.get(
        servidor_dados_url + '/conta/' + conta_id + '/saldo',
        headers={'authorization': auth_token}
    )
    converted_saldo_response = saldo_response.json()
    return converted_saldo_response

def _saque(conta_id, auth_token, valor):
    converted_saldo_response = _saldo(conta_id, auth_token, valor)

    # Retira valor do saque no saldo
    novo_saldo = int(converted_saldo_response['saldo']) - int(valor)

    # Atualiza saldo
    deposito_response = requests.put(
        servidor_dados_url + '/conta/' + conta_id + '/saldo/' + str(novo_saldo),
        headers={'authorization': auth_token}
    )

    print(deposito_response)
    converted_deposito_response = deposito_response.json()

    return converted_deposito_response

def _deposito(conta_id, auth_token, valor):
    # Retorna saldo
    converted_saldo_response = _saldo(conta_id, auth_token, valor)

    # Acrescenta valor do depósito no saldo
    novo_saldo = int(converted_saldo_response['saldo']) + int(valor)

    # Atualiza saldo
    deposito_response = requests.put(
        servidor_dados_url + '/conta/' + conta_id + '/saldo/' + str(novo_saldo),
        headers={'authorization': auth_token}
    )

    print(deposito_response)
    converted_deposito_response = deposito_response.json()

    return converted_deposito_response

@app.route("/")
def index():
    return 'Hello World!'

# Aumenta o saldo da conta <conta_id> pelo valor <valor> e retorna nada
@app.put('/deposito/<conta_id>/<valor>')
def deposito(conta_id, valor):

    auth_token = get_auth_token(int(conta_id))

    if (auth_token != None):
        try:
            return _deposito(conta_id, auth_token, valor)
        except:
            raise_server_error()
    else:
        raise_not_authorized()

# Diminui o saldo da conta <conta_id> pelo valor <valor> e retorna nada
@app.put('/saque/<conta_id>/<valor>')
def saque(conta_id, valor):
    auth_token = get_auth_token(int(conta_id))

    if (auth_token != None):
        try:
            return _saque(conta_id, auth_token, valor)
        except:
            raise_server_error()
    else:
        raise_not_authorized()

# Retorna o saldo da conta <conta_id>
@app.get('/saldo/<conta_id>')
def saldo(conta_id):

    auth_token = get_auth_token(int(conta_id))

    if auth_token != None:
        try:
            return _saldo(conta_id, auth_token)
        except:
            raise_server_error()
    else:
        raise_not_authorized()

# Transferência da conta <conta_origem> para a conta <conta_dest> do valor <valor>
@app.put('/transferencia/<conta_origem>/<conta_dest>/<valor>')
def transferencia(conta_origem, conta_dest, valor):
    #TODO
    return {
        'operation': 'transferencia',
        'conta_origem': conta_origem,
        'conta_dest': conta_dest,
        'valor': valor
    }

