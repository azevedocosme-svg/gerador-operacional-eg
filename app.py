import streamlit as st
import pandas as pd

st.set_page_config(page_title="SIGOT", layout="wide")

st.title("🚀 SIGOT")
st.subheader("Sistema Inteligente de Gestão Operacional de Transportes")

arquivo = st.file_uploader(
    "📥 Importar Relatório Excel",
    type=["xlsx"]
)

if arquivo:

    df = pd.read_excel(arquivo)

    st.success("✅ Arquivo carregado com sucesso")

    st.markdown("## 📋 COLUNAS ENCONTRADAS")
    st.write(df.columns.tolist())

    # =========================
    # CONSOLIDAÇÃO POR OT
    # =========================

    df_consolidado = df.drop_duplicates(subset=["OT"])

    total_veiculos = len(df_consolidado)

    # =========================
    # IDENTIFICAR EXTERNAS
    # =========================

    palavras_externa = [
        "CAMARIM",
        "FIGURINO",
        "FURGÃO",
        "PICK",
        "BLINDADO"
    ]

    mask_externa = df_consolidado["Tipo de Veículo"].astype(str).str.upper().str.contains(
        "|".join(palavras_externa),
        na=False
    )

    externas = df_consolidado[mask_externa]

    total_externas = externas["Programa"].nunique()

    # =========================
    # CAMARINS
    # =========================

    mask_camarim = df_consolidado["Tipo de Veículo"].astype(str).str.upper().str.contains(
        "CAMARIM",
        na=False
    )

    total_camarim = len(df_consolidado[mask_camarim])

    # =========================
    # FIGURINO
    # =========================

    mask_figurino = df_consolidado["Tipo de Veículo"].astype(str).str.upper().str.contains(
        "FIGURINO",
        na=False
    )

    total_figurino = len(df_consolidado[mask_figurino])

    # =========================
    # PRESTADORES
    # =========================

    prestadores = (
        df_consolidado["Prestador do Motorista"]
        .value_counts()
        .reset_index()
    )

    prestadores.columns = ["Prestador", "Quantidade"]

    # =========================
    # DASHBOARD
    # =========================

    st.markdown("---")

    st.markdown("# 📊 DASHBOARD OPERACIONAL")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🚚 Veículos", total_veiculos)
    col2.metric("🎬 Externas", total_externas)
    col3.metric("🎭 Camarins", total_camarim)
    col4.metric("👗 Figurinos", total_figurino)

    # =========================
    # PRESTADORES
    # =========================

    st.markdown("---")

    st.markdown("# 🚛 PRESTADORES")

    st.dataframe(prestadores)

    # =========================
    # BOLETIM EXTERNAS
    # =========================

    st.markdown("---")

    st.markdown("# 🚚 BOLETIM EXTERNAS")

    for programa in externas["Programa"].dropna().unique():

        grupo = externas[externas["Programa"] == programa]

        horario = pd.to_datetime(
            grupo["Data Hora"],
            errors="coerce"
        ).min()

        if pd.isna(horario):
            horario_formatado = "Não informado"
        else:
            horario_formatado = horario.strftime("%d/%m/%Y %H:%M")

        total_operacao = len(grupo)

        st.markdown("━━━━━━━━━━━━━━━━━━━━━━")

        st.markdown(f"## 🎬 {programa}")

        st.markdown(f"⏰ Início: {horario_formatado}")

        st.markdown(f"🚘 Total da operação: {total_operacao}")

        tipos = grupo["Tipo de Veículo"].value_counts()

        for tipo, qtd in tipos.items():
            st.write(f"🚘 {qtd:02d} {tipo}")
