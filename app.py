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

    gerar_externas = st.checkbox("Gerar Externas", value=True)
    gerar_caravanas = st.checkbox("Gerar Caravanas", value=True)
    gerar_alertas = st.checkbox("Gerar Alertas", value=True)

    if st.button("🚀 PROCESSAR"):

        # =========================
        # EXTERNAS
        # =========================

        if gerar_externas:

            st.header("🚚 BOLETIM EXTERNAS")

            palavras_externa = [
                "camarim",
                "figurino",
                "furgão",
                "pickup",
                "pick-up"
            ]

            externas = df[
                df["Tipo de Veículo"]
                .astype(str)
                .str.lower()
                .str.contains("|".join(palavras_externa))
            ]

            grupos = externas.groupby("Programa")

            for programa, grupo in grupos:

                st.subheader(f"🎬 {programa}")

                horario = grupo["Data Hora"].min()

                st.write(f"⏰ Horário inicial: {horario}")

                contagem = (
                    grupo["Tipo de Veículo"]
                    .value_counts()
                )

                for veiculo, qtd in contagem.items():
                    st.write(f"🚘 {qtd:02d} {veiculo}")

                st.divider()
