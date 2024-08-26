# Projeto de Validação de Dados e Criação de Tabelas de Vendas

Este repositório contém scripts e configurações para um teste técnico da Dataholds, focado na criação de tabelas de vendas e validação de dados.

## Estrutura do Repositório

- `./data`: Diretório destinado ao armazenamento de dados utilizados ou gerados pelo projeto.

- `./logs`: Diretório onde os logs de execução serão armazenados.

- `.env`: variveis de conexão com o banco de dados postegreSQL.

- `create_sales_data_with_dates.sql`: Script de criação da tabela sales_data_with_dates.

- `main.py`: Script principal que orquestra a execução dos demais scripts do projeto.

- `requirements.txt`: Lista de dependências Python necessárias para executar o projeto.

- `schema_validation.py`: Script Python para validação de esquema de dados usando Pandera.

## Requisitos

Certifique-se de ter o Python instalado em seu sistema. Para instalar as dependências do projeto, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

## Ordem de Execução 

Para rodar todo o processo de importação é necessario rodar o script `main.py`

## Execução via Docker

Criação da imagem docker

```bash
docker build --tag sales-data-import:latest .
```
Criação do conteiner

```bash
docker run -d \
  --name import-sales \
  -v $(pwd)/logs:/app/logs \
  sales-data-import:latest
```