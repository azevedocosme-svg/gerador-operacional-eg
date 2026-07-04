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

    st.subheader("📊 Prévia do Relatório")
    st.dataframe(df.head())

    gerar_externas = st.checkbox("Gerar Externas", value=True)
    gerar_caravanas = st.checkbox("Gerar Caravanas", value=True)
    gerar_alertas = st.checkbox("Gerar Alertas", value=True)

    if st.button("🚀 PROCESSAR"):

        st.subheader("🎬 PRODUÇÕES IDENTIFICADAS")

        if "Programa" in df.columns:

            programas = (
                df["Programa"]
                .dropna()
                .astype(str)
                .unique()
            )

            for programa in programas:
                st.success(programa)

        else:
            st.error("❌ Coluna 'Programa' não encontrada.")
