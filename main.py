import pandas as pd
from loguru import logger
from datetime import datetime
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from schema_validation import schema_validation
from sql_validation_table import validarTabela
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

        logger.info("convertendo campos de dados......")
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

        logger.info("subindo dados na tabela sales_data_with_dates")

        df_sales_stage.to_sql(
            name="sales_data_with_dates",
            con=postgre_engine,
            index=False,
            if_exists='append',
            chunksize=100
        )
        logger.success(f"Importação finalizada, {len(df_sales_stage)} linhas incluidas na tabela sales_data_with_dates")
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
