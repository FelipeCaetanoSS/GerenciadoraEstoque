import datetime
import streamlit as st
import json

def carregar_dados():
    try:
        with open("CatalogoProdutos.json", "r") as arquivo:
            st.session_state.catalogo_produtos = json.load(arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.catalogo_produtos = {}
    try:
        with open("HistoricoVendas.json", "r") as arquivo:
            st.session_state.historico_vendas = json.load(arquivo)

    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.historico_vendas = []
def salvar_dados():
    with open("CatalogoProdutos.json", "w") as arquivo:
        json.dump(st.session_state.catalogo_produtos, arquivo, indent = 4)
    with open("HistoricoVendas.json", "w") as arquivo:
        json.dump(st.session_state.historico_vendas, arquivo, indent = 4)

st.set_page_config(page_title="Gerenciador de estoque", page_icon="✍️", layout="centered")
st.title("Gerenciador de estoque 📦")

if 'catalogo_produtos' not in st.session_state:
    carregar_dados()

tab1, tab2, tab3 = st.tabs(["Cadastrar Produtos"," Realizar Venda", "Visualizar Historico"])

with tab1:
    st.header("📋 Cadastrar Produtos")
    nome_prod = st.text_input("Nome do Produto").capitalize()
    preco_prod = st.number_input("Preço (R$)", min_value=0.0, format="%.2f")
    estoque = st.number_input("Quantidade em Estoque", min_value=0, step=1)

    if st.button("Cadastrar"):
        if nome_prod.strip() == "":
            st.error("⚠️ O nome do produto não pode estar vazio.")
        elif preco_prod <= 0:
            st.error("⚠️ O preço deve ser maior que zero.")
        elif estoque <= 0:
            st.error("⚠️ O estoque não pode ser negativo.")
        else:
            st.session_state.catalogo_produtos[nome_prod] = {"preço": preco_prod, "estoque": estoque}
            salvar_dados()
            st.success(f"Produto {nome_prod} Cadastrado!")

with tab2:
    st.header("📈 Realizar Venda")
    if not st.session_state.catalogo_produtos:
        st.info("Nenhum produto cadastrado")
    else:
        produto_nomes = list(st.session_state.catalogo_produtos.keys())
        nome_produto = st.selectbox("Selecione o produto:", produto_nomes)
        qtd = st.number_input("Quantidade", step = 1)
        if  st.button("Finalizar venda"):
            if nome_produto in st.session_state.catalogo_produtos and qtd > 0:
                if st.session_state.catalogo_produtos[nome_produto]["estoque"] >= qtd:
                    total = st.session_state.catalogo_produtos[nome_produto]["preço"] * qtd
                    st.session_state.catalogo_produtos[nome_produto]["estoque"] -= qtd
                    venda = {
                    "produto": nome_produto,
                    "quantidade": qtd,
                    "total": total,
                    "data": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    }
                    st.session_state.historico_vendas.append(venda)
                    salvar_dados()
                    st.success(f"Venda de {qtd} {nome_produto}. Valor total: R${total:.2f}")
                else:
                    st.error("Estoque insuficiente.")
            else:
                st.error("Produto não selecionado ou quantidade insuficiente.")

with tab3:
    st.header("📜 Histórico de Vendas")
    if st.button("Ver catalogo de produtos"):
        produtos_para_exibir = []
        for nome, dados in st.session_state.catalogo_produtos.items():
            produtos_para_exibir.append({
                    "Produto": nome,
                    "Preço": dados['preço'],
                    "Estoque": dados['estoque'],
                    })
        if produtos_para_exibir:
            st.dataframe(produtos_para_exibir, use_container_width=True)
        else:
            st.info("Nenhum produto cadastrado.")
    if st.button("Ver histórico de vendas"):
        st.dataframe(st.session_state.historico_vendas)