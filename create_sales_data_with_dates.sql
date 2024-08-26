CREATE TABLE public.sales_data_with_dates(
	data_venda date,
	numero_nota int,
	codigo_produto char(5),
	descricao_produto varchar(30),
	codigo_cliente char(5),
	descricao_cliente varchar(30),
	valor_unitario_produto float(2),
	quantidade_vendida_produto int,
	valor_total float(2),
	custo_da_venda float(2),
	valor_tabela_de_preco_do_produto int
);