import streamlit as st
import pandas as pd

from regras_operacionais import *
from boletim_externas import gerar_boletim

# ==================================================
# CONFIG
# ==================================================

st.set_page_config(
    page_title="SIGOT",
    layout="wide"
)

# ==================================================
# IDENTIFICA CATEGORIA
# ==================================================

def identificar_categoria(tipo):

    tipo = str(tipo).upper()

    for categoria, palavras in CATEGORIAS.items():

        for palavra in palavras:

            if palavra.upper() in tipo:

                return categoria

    return "❓ OUTROS"

# ==================================================
# IDENTIFICA EXTERNA
# ==================================================

def identificar_externa(linha):

    tipo = str(
        linha["Tipo de Veículo"]
    ).upper()

    obs = str(
        linha["Observações"]
    ).upper()

    if (
        "CAMARIM" in tipo
        or "FIGURINO" in tipo
    ):
        return True

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

    st.success(
        "✅ Arquivo carregado com sucesso"
    )

    # ==============================================
    # COLUNAS
    # ==============================================

    st.subheader(
        "📋 COLUNAS ENCONTRADAS"
    )

    st.write(df.columns.tolist())

    # ==============================================
    # DATA
    # ==============================================

    df["Data Hora"] = pd.to_datetime(
        df["Data Hora"],
        errors="coerce"
    )

    # ==============================================
