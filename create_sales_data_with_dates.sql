CREATE TABLE public.fact_sales_with_dates (
    data_venda date,
    numero_nota int primary key,
    codigo_produto char(5),
    codigo_cliente char(5),
    valor_unitario_produto float(2),
    quantidade_vendida_produto int,
    valor_total float(2),
    custo_da_venda float(2),
    FOREIGN KEY (codigo_produto) REFERENCES public.dim_produto (codigo_produto),
    FOREIGN KEY (codigo_cliente) REFERENCES public.dim_cliente (codigo_cliente)
);