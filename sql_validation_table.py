import psycopg2
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

POSTGRE_DATABASE = os.getenv("DATABASE")
POSTGRE_HOST = os.getenv("POSTGRE_HOST")
POSTGRE_PORT = os.getenv("PORT")
POSTGRE_USER = os.getenv("USER")
POSTGRE_PWD = os.getenv("PASSWORD")

conn = None
cur = None


def truncate_table(cur, logger):
    try:
        logger.info("apagando dados da tabela...")
        cur.execute("TRUNCATE TABLE public.sales_data_with_dates")
        logger.sucess("dados apagados com sucesso.")
    except Exception as e:
        logger.exception(e)
        raise


def create_table(cur, logger):
    try:
        logger.info("tabela não existe no banco, criando a tabela...")
        cur.execute(open("create_sales_data_with_dates.sql", "r").read())
        logger.info("tabela criada com sucesso.")
    except Exception as e:
        logger.exception(e)
        raise


def validarTabela(logger):

    try:
        conn = psycopg2.connect(
            dbname=POSTGRE_DATABASE,
            user=POSTGRE_USER,
            password=POSTGRE_PWD,
            host=POSTGRE_HOST,
            port=POSTGRE_PORT,
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(
            """
            SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = %s
            );
        """,
            ("sales_data_with_dates",),
        )

        table_exist = cur.fetchone()[0]

        if not table_exist:
            create_table(cur, logger)
        else:
            truncate_table(cur, logger)

    except Exception as e:
        logger.exception(e)
        raise

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
