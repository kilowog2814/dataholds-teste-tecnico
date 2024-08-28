CREATE TABLE public.dim_produto (
    codigo_produto char(5) primary key,
    descricao_produto varchar(30),
    valor_tabela_de_preco_do_produto int
);