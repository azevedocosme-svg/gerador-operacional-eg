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

    # Converter Data Hora
    df["Data Hora"] = pd.to_datetime(
        df["Data Hora"],
        errors="coerce"
    )

    st.success("✅ Arquivo carregado com sucesso!")

    gerar_externas = st.checkbox("Gerar Externas", value=True)

    if st.button("🚀 PROCESSAR"):

        if gerar_externas:

            st.header("🚚 BOLETIM EXTERNAS")

            palavras = [
                "camarim",
                "figurino",
                "furgão",
                "furgao",
                "pick",
                "blindado"
            ]

            filtro = df["Tipo de Veículo"].astype(str).str.lower()

            externas = df[
                filtro.str.contains("|".join(palavras))
            ]

            grupos = externas.groupby("Programa")

            for programa, grupo in grupos:

                st.subheader(f"🎬 {programa}")

                horario = grupo["Data Hora"].dropna().min()

                if pd.notna(horario):
                    horario_formatado = horario.strftime("%d/%m/%Y %H:%M")
                else:
                    horario_formatado = "Não informado"

                st.write(f"⏰ Horário inicial: {horario_formatado}")

                contagem = (
                    grupo["Tipo de Veículo"]
                    .value_counts()
                )

                for veiculo, qtd in contagem.items():
                    st.write(f"🚘 {qtd:02d} {veiculo}")

                st.divider()
