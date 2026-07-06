import streamlit as st
import pandas as pd
import re

from regras_operacionais import *

# ==================================================
# CONFIGURAÇÃO
# ==================================================

st.set_page_config(
    page_title="SIGOT",
    layout="wide"
)

# ==================================================
# IDENTIFICA CATEGORIA OPERACIONAL
# ==================================================

def identificar_categoria(tipo_veiculo):

    tipo_veiculo = str(tipo_veiculo).upper()

    for categoria, palavras in CATEGORIAS.items():

        for palavra in palavras:

            if palavra.upper() in tipo_veiculo:

                return categoria

    return "❓ OUTROS"

# ==================================================
# TÍTULO
# ==================================================

st.title("🚀 SIGOT")
st.subheader("Sistema Inteligente de Gestão Operacional de Transportes")

# ==================================================
# IMPORTAÇÃO
# ==================================================

arquivo = st.file_uploader(
    "📥 Importar Relatório Excel",
    type=["xlsx"]
)

# ==================================================
# PROCESSAMENTO
# ==================================================

if arquivo:

    df = pd.read_excel(arquivo)

    st.success("✅ Arquivo carregado com sucesso")

    st.subheader("📋 COLUNAS ENCONTRADAS")
    st.write(df.columns.tolist())

    # ==============================================
    # CATEGORIA OPERACIONAL
    # ==============================================

    df["Categoria Operacional"] = df["Tipo de Veículo"].apply(
        identificar_categoria
    )

    # ==============================================
    # DASHBOARD
    # ==============================================

    st.markdown("---")

    st.markdown("# 📊 RESUMO POR CATEGORIA")

    resumo = (
        df["Categoria Operacional"]
        .value_counts()
        .reset_index()
    )

    resumo.columns = [
        "Categoria",
        "Quantidade"
    ]

    st.table(resumo)

    # ==============================================
    # PRÉVIA
    # ==============================================

    st.markdown("---")

    st.subheader("📊 Prévia do Excel")

    st.dataframe(df.head())
