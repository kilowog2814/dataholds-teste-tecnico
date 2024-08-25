import pandera as pa
import pandas as pd


def schema_validation(dataframe: pd.DataFrame):
    schema = pa.DataFrameSchema(
        columns={
            "data_venda": pa.Column(pa.DateTime),
            "numero_nota": pa.Column(int),
            "codigo_produto": pa.Column(str, checks=[pa.Check.str_startswith("P")]),
            "descricao_produto": pa.Column(str),
            "codigo_cliente": pa.Column(str, checks=[pa.Check.str_startswith("C")]),
            "descricao_cliente": pa.Column(str),
            "valor_unitario_produto": pa.Column(float),
            "quantidade_vendida_produto": pa.Column(int),
            "valor_total": pa.Column(float),
            "custo_da_venda": pa.Column(float),
            "valor_tabela_de_preco_do_produto": pa.Column(float),
        }
    )

    return schema(dataframe)
