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

tables_validation_list = [
    {"table": "dim_produto", "sql_file": "create_dim_produtos.sql"},
    {"table": "dim_cliente", "sql_file": "create_dim_clientes.sql"},
    {"table": "fact_sales_with_dates", "sql_file": "create_sales_data_with_dates.sql"},
]


def truncate_table(cur, logger, table_name):
    try:
        cur.execute(f"TRUNCATE TABLE public.{table_name} RESTART IDENTITY CASCADE")

        logger.success(f"dados da tabela {table_name} apagados com sucesso.")
    except Exception as e:
        logger.exception(e)
        raise


def create_table(cur, logger, file_name_sql):
    try:

        cur.execute(open(file_name_sql, "r").read())
        logger.info("tabela criada com sucesso.")
    except Exception as e:
        logger.exception(e)
        raise


def validation_tables(logger):

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

        for table in tables_validation_list:

            cur.execute(
                """
                SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
                );
            """,
                (table["table"],),
            )

            table_exist = cur.fetchone()[0]

            if not table_exist:
                logger.info(
                    f"tabela {table['table']} não existe no banco, criando a tabela..."
                )
                create_table(cur, logger, table["sql_file"])
            else:
                logger.info(f"apagando dados da tabela {table['table']}...")
                truncate_table(cur, logger, table["table"])

    except Exception as e:
        logger.exception(e)
        raise

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
