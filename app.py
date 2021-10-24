from flask import Flask

app = Flask(__name__)

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
    return {
        'saldo': 'saldo',
        'conta_id': conta_id
    }, 200

# Transferência da conta <conta_origem> para a conta <conta_dest> do valor <valor>
@app.put('/transferencia/<conta_origem>/<conta_dest>/<valor>')
def transferencia(conta_origem, conta_dest, valor):
    return {
        'operation': 'transferencia',
        'conta_origem': conta_origem,
        'conta_dest': conta_dest,
        'valor': valor
    }

