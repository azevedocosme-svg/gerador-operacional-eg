import streamlit as st
import pandas as pd
import re

from regras_operacionais import *

st.set_page_config(page_title="SIGOT", layout="wide")

st.title("🚀 SIGOT – Sistema Inteligente de Gestão Operacional de Transportes")

arquivo = st.file_uploader(
    "📥 Importar Relatório Excel",
    type=["xlsx"]
)

if arquivo:

    df = pd.read_excel(arquivo)

    st.success("Arquivo carregado com sucesso!")

    st.subheader("📋 COLUNAS ENCONTRADAS")
    st.write(list(df.columns))

    st.subheader("📊 Prévia do Excel")
    st.dataframe(df.head())
