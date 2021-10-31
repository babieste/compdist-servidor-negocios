from flask import Flask, abort, request, Request
from dotenv import load_dotenv
from os import environ
import requests
import logging

load_dotenv()

servidor_dados_url = environ.get('SERVIDOR_DADOS_URL')
servidor_id = environ.get('SERVIDOR_ID')

app = Flask(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format=f'%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/record.log', mode='w'),
        logging.StreamHandler()
    ]
)

app.logger.info('Inicializando o servidor de negócio {}'.format(servidor_id))

tokens = [
    'secret#1',
    'secret#2',
    'secret#3'
]

num_operacao: int = 0

# Incrementa a quantidade de operações realizadas no servidor
def increment_operation():
    global num_operacao
    num_operacao += 1

def authorize(request: Request):
    received_auth_token = request.headers.get('Authorization')
    auth_token = None
    if received_auth_token in tokens:
        auth_token = received_auth_token
    return auth_token

def raise_server_error():
    response = app.make_response(
        ({'message': 'Não foi possível realizar a operação'}, 500, [('x-server-id', servidor_id)])
    )
    abort(response)

def raise_unauthorized():
    response = app.make_response(
        ({'message': 'Não autorizado'}, 401, [('x-server-id', servidor_id)])
    )
    abort(response)

def _saldo(conta_id, auth_token):
    # Retorna saldo
    response = requests.get(
        servidor_dados_url + '/conta/' + conta_id + '/saldo',
        headers={'authorization': auth_token}
    )

    converted_response = response.json()

    app.logger.debug(str(num_operacao) + ' - SERVIDOR ' + servidor_id + ' - OPERAÇÃO: SALDO - CONTA ' + str(conta_id))

    increment_operation()

    return converted_response, response.status_code

def _saque(conta_id, auth_token, valor):
    saldo_response = _saldo(conta_id, auth_token)[0]

    # Retira valor do saque no saldo
    novo_saldo = int(saldo_response['saldo']) - int(valor)

    # Atualiza saldo
    response = requests.put(
        servidor_dados_url + '/conta/' + conta_id + '/saldo/' + str(novo_saldo),
        headers={'authorization': auth_token}
    )

    converted_response = response.json()

    app.logger.debug(str(num_operacao) + ' - SERVIDOR ' + servidor_id + ' - OPERAÇÃO: SAQUE - CONTA ' + str(conta_id) + ' -  VALOR ' + str(valor))

    increment_operation()

    return converted_response, response.status_code

def _deposito(conta_id, auth_token, valor):
    # Retorna saldo
    saldo_response = _saldo(conta_id, auth_token)[0]

    # Acrescenta valor do depósito no saldo
    novo_saldo = int(saldo_response['saldo']) + int(valor)

    # Atualiza saldo
    response = requests.put(
        servidor_dados_url + '/conta/' + conta_id + '/saldo/' + str(novo_saldo),
        headers={'authorization': auth_token}
    )

    converted_response = response.json()

    app.logger.debug(str(num_operacao) + ' - SERVIDOR ' + servidor_id + ' - OPERAÇÃO: DEPÓSITO - CONTA ' + str(conta_id) + ' -  VALOR ' + str(valor))

    increment_operation()

    return converted_response, response.status_code

@app.route('/')
def index():
    return app.make_response(
        ('Hello World!', [('x-server-id', servidor_id)])
    )

# Aumenta o saldo da conta <conta_id> pelo valor <valor> e retorna nada
@app.put('/deposito/<conta_id>/<valor>')
def deposito(conta_id, valor):
    auth_token = authorize(request)

    if (auth_token != None):
        try:
            response = _deposito(conta_id, auth_token, valor)
            return app.make_response(
                (response[0], response[1], [('x-server-id', servidor_id)])
            )
        except:
            raise_server_error()
    else:
        raise_unauthorized()

# Diminui o saldo da conta <conta_id> pelo valor <valor> e retorna nada
@app.put('/saque/<conta_id>/<valor>')
def saque(conta_id, valor):
    auth_token = authorize(request)

    if (auth_token != None):
        try:
            response = _saque(conta_id, auth_token, valor)
            return app.make_response(
                (response[0], response[1], [('x-server-id', servidor_id)])
            )
        except:
            raise_server_error()
    else:
        raise_unauthorized()

# Retorna o saldo da conta <conta_id>
@app.get('/saldo/<conta_id>')
def saldo(conta_id):
    auth_token = authorize(request)

    if auth_token != None:
        try:
            response = _saldo(conta_id, auth_token)
            return app.make_response(
                (response[0], response[1], [('x-server-id', servidor_id)])
            )
        except:
            raise_server_error()
    else:
        raise_unauthorized()

# Transferência da conta <conta_origem> para a conta <conta_dest> do valor <valor>
@app.put('/transferencia/<conta_origem>/<conta_dest>/<valor>')
def transferencia(conta_origem, conta_dest, valor):
    conta_origem_token = authorize(request)
    conta_dest_token = authorize(request)

    if conta_origem_token != None and conta_dest_token != None:
        try:
            # Saque da conta de origem
            _saque(conta_origem, conta_origem_token, valor)

            # Depósito na conta de destino
            _deposito(conta_dest, conta_dest_token, valor)

            return app.make_response(
                ({'message': 'Transferência realizada.'}, 200, [('x-server-id', servidor_id)])
            )
        except:
            raise_server_error()
    else:
        raise_unauthorized()
