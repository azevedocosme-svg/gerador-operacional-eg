import streamlit as st

st.set_page_config(page_title="Gerador Operacional EG")

st.title("🚀 GERADOR OPERACIONAL EG")

uploaded_file = st.file_uploader(
    "📥 Importar Relatório Excel",
    type=["xlsx"]
)

if uploaded_file:
    st.success("Arquivo carregado com sucesso!")

    gerar_externas = st.checkbox("Gerar Externas", value=True)
    gerar_caravanas = st.checkbox("Gerar Caravanas", value=True)
    gerar_alertas = st.checkbox("Gerar Alertas", value=True)

    if st.button("🚀 PROCESSAR"):
        st.write("Processando relatório operacional...")
