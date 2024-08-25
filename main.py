import pandas as pd
from loguru import logger
from datetime import datetime
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from schema_validation import schema_validation

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

log_path = datetime.today().strftime("%Y/%m/%d/")
log_name = datetime.today().strftime("sales_data_with_dates_%H-%M-%S.log")

logger.add(f"logs/{log_path}/{log_name}")


def main():

    logger.info("iniciando processo.....")
    logger.info(f"abrindo arquivo {DATA_FILE_PATH.split("/")[1]}")
    df_sales_stage = pd.read_excel(DATA_FILE_PATH)

    schema_validation(df_sales_stage)


if __name__ == "__main__":
    main()
