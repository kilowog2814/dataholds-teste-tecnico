# Projeto de Validação de Dados e Criação de Tabelas de Vendas

Este repositório contém scripts e configurações para um teste, focado na criação de tabelas de vendas e validação de dados.

## Estrutura do Repositório

- `./data`: Diretório destinado ao armazenamento de dados utilizados ou gerados pelo projeto.

- `./logs`: Diretório onde os logs de execução serão armazenados.

- `.env`: variveis de conexão com o banco de dados postegreSQL.

- `create_sales_data_with_dates.sql`: Script de criação da tabela fato sales_data_with_dates.

- `create_dim_clientes.sql`: Script de criação da tabela dimensão cliente.

- `create_dim_produto.sql`: Script de criação da tabela dimensão produto.

- `main.py`: Script principal que orquestra a execução dos demais scripts do projeto.

- `requirements.txt`: Lista de dependências Python necessárias para executar o projeto.

- `schema_validation.py`: Script Python para validação de esquema de dados usando Pandera.

- `sql_validation_table.py`: Script de validação das tabelas existe ou não no banco.

## Requisitos

O projeto foi desenvolvido na versão 3.12.5 do python.

Certifique-se de ter o Python instalado em seu sistema. Para instalar as dependências do projeto, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

## Ordem de Execução 

Para iniciar o processo de importação, siga as etapas:

1. Incluir os dados de acesso ao banco de dados no arquivo `.env`
2. Gerar o ambiente com as bibliotecas do `requirements.txt`
3. Rodar o script `main.py` disponivel no repositorio


## Execução via Docker

Criação da imagem docker

```bash
docker build --tag sales-data-import:latest .
```
Criação do conteiner

```bash
docker run --rm --name import_sales -v ${PWD}/logs:/app/logs sales-data-import:latest
```
