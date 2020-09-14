# Safra MEI - Backend

Esta pasta contém os scripts Python utilizados para disponibilização de um serviço listener de Webhooks. O serviço faz uso do framework Flask.

## Requisitos

Algumas bibliotecas precisam ser instaladas no ambiente Python para o devido funcionamento da ferramenta:
`flask`
`requests`
`base64`
`json`
`enum`

Além disso, a porta `5000` local precisa estar disponível para acesso (porta padrão do Flask).

## Integrações

A aplicação utiliza os seguintes endpoints da API Technee disponibilizada para o projeto, sem contar a necessária verificação de token OAuth:

### Consulta dados da conta
`GET [host]/open-banking/v1/accounts/{accountId}`

### Consulta saldo da conta
`GET [host]/open-banking/v1/accounts/{accountId}/balances`

## Endpoints

As funcionalidades disponibilizadas pelas aplicações são como seguem:

| Endpoint            | Parâmetros        | Descrição                                                                          |
|---------------------|-------------------|------------------------------------------------------------------------------------|
| `POST [host]/conta` | conta_id (string) | Retorna detalhes da conta acessando a aplicação, se houver (nome, apelido e saldo) |
| `POST [host]/emprestimo` | valor_solicitado (número), numero_meses (número), taxa_juros (número) | Usando o valor a ser requisitado como crédito, a quantidade de tempo para pagamento e a taxa de juros atual, retorna o valor da prestação mensal a ser pago |
| `POST [host]/investimentos` | conta_id (string) | Retorna detalhes dos investimentos da conta acessando a aplicação, se houver (conca corrente, LCA1, LCA2, LCA3, Poupança) |
| `POST [host]/analise/perfil-investidor` | soma_respostas_formulario (número) | Usando o somatório fornecido pelo formulário de verificação de perfil de investidor, retorna os detalhes do perfil associado |
| `POST [host]/simulacao/renda-fixa` | valor_investimento (número), numero_meses (número) | Usando o valor inicial de investimento e a quantidade de tempo a manter investido, retorna os valores finais do saldo em cada um dos possíveis investimentos (LCA1, LCA2, LCA3, Poupança) |

## Execução

Para subir a aplicação, executar o script app.py, ou dentro do environment, executar `flask run`