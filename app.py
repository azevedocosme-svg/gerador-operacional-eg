import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gerador Operacional EG")

st.title("🚀 GERADOR OPERACIONAL EG")

uploaded_file = st.file_uploader(
    "📥 Importar Relatório Excel",
    type=["xlsx"]
)

if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.success("✅ Arquivo carregado com sucesso!")

    st.subheader("📋 COLUNAS ENCONTRADAS")

    for col in df.columns:
        st.write(col)

    st.subheader("📊 Prévia do Excel")
    st.dataframe(df.head())
