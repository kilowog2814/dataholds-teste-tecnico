import pandas as pd
from loguru import logger
from datetime import datetime
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from schema_validation import schema_validation
from sql_validation_table import validation_tables
import numpy as np
import time

load_dotenv()

POSTGRE_DATABASE = os.getenv("DATABASE")
POSTGRE_HOST = os.getenv("POSTGRE_HOST")
POSTGRE_PORT = os.getenv("PORT")
POSTGRE_USER = os.getenv("USER")
POSTGRE_PWD = os.getenv("PASSWORD")

DATA_FILE_PATH = "data/sales_data_with_dates.xlsx"

postgre_engine = create_engine(
    f"postgresql://{POSTGRE_USER}:{POSTGRE_PWD}@{POSTGRE_HOST}:{POSTGRE_PORT}/{POSTGRE_DATABASE}"
)

log_path = datetime.today().strftime("%Y/%m/%d")
log_name = datetime.today().strftime("sales_data_with_dates_%H-%M-%S.log")

logger.add(f"logs/{log_path}/{log_name}")


def main():

    inicio = time.time()
    logger.info("iniciando processo.....")

    try:
        logger.info(f"abrindo arquivo {DATA_FILE_PATH.split("/")[1]}")
        df_sales_stage = pd.read_excel(DATA_FILE_PATH,
                                       dtype={
                                            'numero_nota': np.int64,
                                            'codigo_produto': str,
                                            'descricao_produto': str,
                                            'codigo_cliente': str,
                                            'descricao_cliente': str,
                                            'valor_unitario_produto': np.float64,
                                            'quantidade_vendida_produto': np.int64,
                                            'valor_total': np.float64,
                                            'custo_da_venda': np.float64,
                                            'valor_tabela_de_preco_do_produto':np.float64
                                        })

        logger.info("ajustando campo de data......")
        df_sales_stage['data_venda'] = pd.to_datetime(df_sales_stage['data_venda'],
                                                      dayfirst=True,
                                                      errors="coerce")

        logger.info("removendo duplicados......")
        df_sales_stage = df_sales_stage.drop_duplicates()

        logger.info("removendo dados com erro......")

        df_sales_stage = df_sales_stage.dropna()

        logger.info("validando schema.....")
        schema_validation(df_sales_stage)
        logger.success("dados validados")

        logger.info("validando tabela no banco.....")

        validation_tables(logger)

        logger.success("tabelas validadas.....")

        logger.info("subindo dados na tabela dim_produtos")

        df_dim_produtos = df_sales_stage[['codigo_produto', 'descricao_produto',
                                          'valor_tabela_de_preco_do_produto']].drop_duplicates()
        
        df_dim_produtos.to_sql(
            name="dim_produto",
            con=postgre_engine,
            index=False,
            if_exists='append',
            chunksize=100
        )

        logger.success(f"Importação finalizada, {len(df_dim_produtos)} linhas incluidas na tabela dim_produtos")

        df_dim_clientes = df_sales_stage[['codigo_cliente', 'descricao_cliente']].drop_duplicates()
       
        df_dim_clientes.to_sql(
            name="dim_cliente",
            con=postgre_engine,
            index=False,
            if_exists='append',
            chunksize=100
        )
  
        logger.info("subindo dados na tabela dim_clientes")
        logger.success(f"Importação finalizada, {len(df_dim_produtos)} linhas incluidas na tabela dim_clientes")

        logger.info("subindo dados na tabela fact_sales_with_dates")

        fact_sales_with_dates = df_sales_stage.drop(
            columns=['descricao_produto',
                     'valor_tabela_de_preco_do_produto',
                     'descricao_cliente'])
        
        fact_sales_with_dates.to_sql(
            name="fact_sales_with_dates",
            con=postgre_engine,
            index=False,
            if_exists='append',
            chunksize=100
        )
        logger.success(f"Importação finalizada, {len(fact_sales_with_dates)} linhas incluidas na tabela fact_sales_with_dates")
        
        logger.success("Processo finalizado!!!")


    except FileNotFoundError as file_error:
        logger.exception(file_error)
        raise
    except Exception as other_errors:
        logger.exception(other_errors)
        raise
    finally:
        execution_time = time.time() - inicio
        logger.debug(f"tempo de execução: {execution_time:.2f} segundos")


if __name__ == "__main__":
    main()
