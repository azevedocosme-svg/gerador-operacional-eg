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
# IDENTIFICA EXTERNAS
# ==================================================

def identificar_externa(linha):

    tipo = str(linha["Tipo de Veículo"]).upper()
    obs = str(linha["Observações"]).upper()

    # EXTERNA COM CAMARIM

    if (
        "CAMARIM" in tipo
        or "FIGURINO" in tipo
    ):

        return True

    # EXTERNA POR OBSERVAÇÃO

    for palavra in PALAVRAS_EXTERNA:

        if palavra in obs:

            return True

    return False

# ==================================================
# TÍTULO
# ==================================================

st.title("🚀 SIGOT")
st.subheader(
    "Sistema Inteligente de Gestão Operacional de Transportes"
)

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

    # ==============================================
    # COLUNAS
    # ==============================================

    st.subheader("📋 COLUNAS ENCONTRADAS")
    st.write(df.columns.tolist())

    # ==============================================
    # CONVERTE DATAS
    # ==============================================

    df["Data Hora"] = pd.to_datetime(
        df["Data Hora"],
        errors="coerce"
    )

    # ==============================================
    # CATEGORIA OPERACIONAL
    # ==============================================

    df["Categoria Operacional"] = df[
        "Tipo de Veículo"
    ].apply(
        identificar_categoria
    )

    # ==============================================
    # IDENTIFICA EXTERNAS
    # ==============================================

    df["Externa"] = df.apply(
        identificar_externa,
        axis=1
    )

    # ==============================================
    # DASHBOARD
    # ==============================================

    st.markdown("---")

    total_veiculos = len(df)

    total_externas = len(
        df[df["Externa"] == True]
    )

    total_camarins = len(
        df[
            df["Categoria Operacional"]
            == "🎭 CAMARIM"
        ]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🚚 Veículos",
        total_veiculos
    )

    col2.metric(
        "🎬 Externas",
        total_externas
    )

    col3.metric(
        "🎭 Camarins",
        total_camarins
    )

    # ==============================================
    # RESUMO OPERACIONAL
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
    # BOLETIM EXTERNAS
    # ==============================================

    st.markdown("---")

    st.markdown("# 🚚 BOLETIM DE EXTERNAS")

    externas = df[
        df["Externa"] == True
    ]

    if len(externas) > 0:

        programas = externas[
            "Programa"
        ].dropna().unique()

        for programa in programas:

            grupo = externas[
                externas["Programa"] == programa
            ]

            # ======================================
            # HORÁRIO
            # ======================================

            horario = grupo[
                "Data Hora"
            ].min()

            horario_formatado = (
                horario.strftime("%d/%m/%Y %H:%M")
                if pd.notnull(horario)
                else "Sem horário"
            )

            # ======================================
            # EXIBE
            # ======================================

            st.markdown(
                "━━━━━━━━━━━━━━━━━━━━━━"
            )

            st.markdown(
                f"### 🎬 {programa}"
            )

            st.markdown(
                f"⏰ Início: {horario_formatado}"
            )

            st.markdown(
                f"🚘 Total veículos: {len(grupo)}"
            )

            # ======================================
            # RESUMO VEÍCULOS
            # ======================================

            resumo_veiculos = (
                grupo[
                    "Categoria Operacional"
                ]
                .value_counts()
            )

            for veiculo, qtd in resumo_veiculos.items():

                st.markdown(
                    f"🚘 {qtd} {veiculo}"
                )

    # ==============================================
    # PRÉVIA
    # ==============================================

    st.markdown("---")

    st.subheader("📊 Prévia do Excel")

    st.dataframe(df.head())
