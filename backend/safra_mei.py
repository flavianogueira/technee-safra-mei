import requests
import base64
import json
from enum import Enum

client_id = 'b5fb1e3b36714ad0a08e9fd541d00160'
client_secret = 'a70413b9-8837-47df-885e-3d0449feabf5'
token = ""

class Perfil(Enum):
    CONSERVADOR = "Fundo de Renda Fixa / Títulos Públicos / Certicado de Depósito Bancário (CDB) / " \
                  "Letra de Crédito Imobiliário (LCI) / Letra de Crédito do Agronegócio (_lca) / " \
                  "Certicado de Recebíveis Imobiliários (CRI) / Certicado de Recebíveis do Agronegócio (CRA) / Debêntures / Letras de Câmbio (LC)."
    MODERADO = "Todos os produtos e operações do perl Conservador, / Mercado à vista em Bolsa de Valores / " \
               "Posições doadoras em empréstimo de ações (BTC) / Fundos Multimercado sem alavancagem / Clube de Investimento / " \
               "Fundo de Ações / Fundo Cambial / Fundo de Investimento em Direitos Creditórios (FIDC) / " \
               "Fundo de Investimento em Participações (FIP) / Fundos de Investimento Imobiliários (FII) / " \
               "Ouro à vista / Brazilian Depositary Receipt (BDR)."
    ARROJADO  = "Todos os produtos e operações indicados ao perl Moderado / Derivativos / " \
                "Posições tomadoras em empréstimos de ações (BTC) / Fundo Multimercado com Alavancagem."


def calcula_valor_prestacao(valor_solicitado, numero_meses, taxa_juros):

    valor_parcela = (valor_solicitado/numero_meses)*taxa_juros
    valor_final = valor_parcela*numero_meses

    return {"valor_parcela": valor_parcela, "valor_final": valor_final}


def calcula_valores_renda_fixa(valor_investimento, numero_meses):

    taxa_lca1 = 1.3
    taxa_lca2 = 2.2
    taxa_lca3 = 3
    taxa_poup = 1.05

    rendimento_lca1 = (valor_investimento*taxa_lca1)
    rendimento_lca2 = (valor_investimento*taxa_lca2)
    rendimento_lca3 = (valor_investimento*taxa_lca3)
    rendimento_poup = (valor_investimento*taxa_poup)

    rendimentos = {
        "rendimento_lca1": rendimento_lca1,
        "rendimento_lca2": rendimento_lca2,
        "rendimento_lca3": rendimento_lca3,
        "rendimento_poup": rendimento_poup
    }

    return rendimentos

def dados_conta(conta):

    novo_token = verificar_token(conta,token)
    nomes_conta = nome_conta(conta,novo_token)
    saldo_conta = saldo(conta,novo_token)
    
    resultados_conta = {
        "nome": nomes_conta[0],
        "apelido": nomes_conta[1],
        "saldo": saldo_conta,
    }

    return resultados_conta

def retorno_investimentos(conta):

    novo_token = verificar_token(conta,token)
    saldo_conta = saldo(conta,novo_token)
    saldo_lca1 = valor_lca1(conta,novo_token)
    saldo_lca2 = valor_lca2(conta,novo_token)
    saldo_lca3 = valor_lca3(conta,novo_token)
    saldo_poup = valor_poup(conta,novo_token)
    
    investimentos = {
        "saldo_conta": saldo_conta,
        "saldo_lca1": saldo_lca1,
        "saldo_lca2": saldo_lca2,
        "saldo_lca3": saldo_lca3,
        "saldo_poup": saldo_poup
    }

    return investimentos


def analisa_perfil_investidor(soma_respostas_formulario):
    if(soma_respostas_formulario > 0 and soma_respostas_formulario <= 9):
        perfil_investidor = {"classe_pontuacao": soma_respostas_formulario, "perfil": Perfil.CONSERVADOR.name, "operacoes_indicadas": Perfil.CONSERVADOR.value}
    elif(soma_respostas_formulario > 9 and soma_respostas_formulario<=25):
        perfil_investidor = {"classe_pontuacao": soma_respostas_formulario, "perfil": Perfil.MODERADO.name, "operacoes_indicadas": Perfil.MODERADO.value}
    else:
        perfil_investidor = {"classe_pontuacao": soma_respostas_formulario, "perfil": Perfil.ARROJADO.name, "operacoes_indicadas": Perfil.ARROJADO.value}

    return perfil_investidor


def tokenheader(token):
    return {"Authorization": "Bearer "+token}


def verificar_token(conta,token):
    status = requests.get('https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/open-banking/v1/accounts/'+conta, headers=tokenheader(token)).status_code
    if status != "200":
        return pegar_token()
    else:
        return token


def pegar_token():
    stringrequest = base64.b64encode((client_id+':'+client_secret).encode('ascii')).decode('ascii')
    authheader = {"Authorization": "Basic "+stringrequest, "content-type": "application/x-www-form-urlencoded"}
    body = "grant_type=client_credentials&scope=urn:opc:resource:consumer::all"
    json_token = requests.post('https://idcs-902a944ff6854c5fbe94750e48d66be5.identity.oraclecloud.com/oauth2/v1/token', headers=authheader, data=body).json()
    
    return json_token['access_token']


def nome_conta(conta, token):
    saldo = requests.get('https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/open-banking/v1/accounts/'+conta, headers=tokenheader(token)).json()
    nome_cliente = saldo['Data']['Account'][0]['Account']['Name']
    apelido_cliente = saldo['Data']['Account'][0]['Nickname']
    
    return [nome_cliente, apelido_cliente]


def saldo(conta, token):
    saldo = requests.get('https://af3tqle6wgdocsdirzlfrq7w5m.apigateway.sa-saopaulo-1.oci.customer-oci.com/fiap-sandbox/open-banking/v1/accounts/'+conta+'/balances', headers=tokenheader(token)).json()
    saldo_reais = saldo['Data']['Balance'][0]['Amount']['Amount']
    
    return saldo_reais


def valor_lca1(conta, token):
    valor = {"Data": {"Balance": [{"AccountId": conta, "Amount": {"Amount": "210.00", "Currency": "BRL"},}]}}
    valor_reais = valor['Data']['Balance'][0]['Amount']['Amount']
    
    return valor_reais


def valor_lca2(conta, token):
    valor = {"Data": {"Balance": [{"AccountId": conta, "Amount": {"Amount": "320.00", "Currency": "BRL"},}]}}
    valor_reais = valor['Data']['Balance'][0]['Amount']['Amount']
    
    return valor_reais


def valor_lca3(conta, token):
    valor = {"Data": {"Balance": [{"AccountId": conta, "Amount": {"Amount": "150.00", "Currency": "BRL"},}]}}
    valor_reais = valor['Data']['Balance'][0]['Amount']['Amount']
    
    return valor_reais


def valor_poup(conta, token):
    valor = {"Data": {"Balance": [{"AccountId": conta, "Amount": {"Amount": "50.00", "Currency": "BRL"},}]}}
    valor_reais = valor['Data']['Balance'][0]['Amount']['Amount']
    
    return valor_reais