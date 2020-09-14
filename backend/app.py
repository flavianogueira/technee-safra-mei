from flask import Flask, request
from safra_mei import *

app = Flask(__name__)

@app.route("/")
def teste():
    welcome = "Bem vindo ao SafraMEI!"
    return welcome

@app.route("/conta", methods=["POST"])
def conta():
    body = request.get_json()
    detalhes_conta = dados_conta(body["conta_id"])
    return detalhes_conta

@app.route("/emprestimo", methods=["POST"])
def emprestimo():
    body = request.get_json()
    valor_prestacao = calcula_valor_prestacao(body["valor_solicitado"], body["numero_meses"], body["taxa_juros"])
    return valor_prestacao

@app.route("/investimentos", methods=["POST"])
def investimentos():
    body = request.get_json()
    investimentos_total = retorno_investimentos(body["conta_id"])
    return investimentos_total

@app.route("/simulacao/renda-fixa", methods=["POST"])
def simulando_renda_fixa():
    body = request.get_json()
    rendimentos_fixos = calcula_valores_renda_fixa(body["valor_investimento"], body["numero_meses"])
    return rendimentos_fixos

@app.route("/analise/perfil-investidor", methods=["POST"])
def analisando_perfil_investidor():
    body = request.get_json()
    perfil = analisa_perfil_investidor(body["soma_respostas_formulario"])
    return perfil


if __name__ == '__main__':
    app.run()