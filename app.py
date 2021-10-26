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
    response = requests.get(
        servidor_dados_url + '/conta/' + conta_id + '/saldo',
        headers={'authorization': auth_token}
    )
    converted_response = response.json()
    return converted_response

def _saque(conta_id, auth_token, valor):
    saldo_response = _saldo(conta_id, auth_token, valor)

    # Retira valor do saque no saldo
    novo_saldo = int(saldo_response['saldo']) - int(valor)

    # Atualiza saldo
    response = requests.put(
        servidor_dados_url + '/conta/' + conta_id + '/saldo/' + str(novo_saldo),
        headers={'authorization': auth_token}
    )
    converted_response = response.json()
    print('saque:' + str(converted_response))
    return converted_response

def _deposito(conta_id, auth_token, valor):
    # Retorna saldo
    saldo_response = _saldo(conta_id, auth_token, valor)

    # Acrescenta valor do depósito no saldo
    novo_saldo = int(saldo_response['saldo']) + int(valor)

    # Atualiza saldo
    response = requests.put(
        servidor_dados_url + '/conta/' + conta_id + '/saldo/' + str(novo_saldo),
        headers={'authorization': auth_token}
    )
    converted_response = response.json()
    print('deposito:' + str(converted_response))
    return converted_response

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

    conta_origem_token = get_auth_token(int(conta_origem))
    print('conta_origem_token ' + conta_origem_token)
    conta_dest_token = get_auth_token(int(conta_dest))
    print('conta_dest_token ' + conta_dest_token)

    if conta_origem_token != None and conta_dest_token != None:
        try:
            # Saque da conta de origem
            _saque(conta_origem, conta_origem_token, valor)

            # Depósito na conta de destino
            _deposito(conta_dest, conta_dest_token, valor)

            return app.make_response(
                ({'message': 'Transferência realizada.'}, 200)
            )
        except:
            raise_server_error()
    else:
        raise_not_authorized()
