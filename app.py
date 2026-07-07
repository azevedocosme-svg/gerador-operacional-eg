import streamlit as st
import pandas as pd

from regras_operacionais import *

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
# EXTRAI APRESENTAÇÃO
# ==================================================

def extrair_apresentacao(texto):

    texto = str(texto).upper()

    palavras = [
        "RECUO MG1",
        "RECUO DO MG1",
        "RECUO MG3",
        "RECUO DO MG3",
        "COPA MG1",
        "COPA MG3",
        "PORTARIA 1",
        "PORTARIA 2",
        "PORTARIA 3",
        "PORTARIA 4",
        "PA 11",
        "PA 20",
        "CDE"
    ]

    for item in palavras:

        if item in texto:
            return item

    return ""

# ==================================================
# EXTRAI LOCAÇÃO
# ==================================================

def extrair_locacao(texto):

    texto = str(texto).upper()

    locais = [

        "FAZENDA INDIANA",
        "MUSAL",
        "MERCADO SUPERBOM",
        "SUPERBOM",
        "BAR SALETE",
        "ATERRO DO FLAMENGO",
        "BOSQUE DA GLORIA",
        "TAVARES BASTOS",
        "TIJUCA",
        "CATETE"

    ]

    for item in locais:

        if item in texto:
            return item

    return ""

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

    st.subheader(
        "📋 COLUNAS ENCONTRADAS"
    )

    st.write(df.columns.tolist())

    df["Data Hora"] = pd.to_datetime(
        df["Data Hora"],
        errors="coerce"
    )

    # ==================================================
    # CHAVE
    # ==================================================

    df["Chave Operacional"] = (

        df["OT"].astype(str)

        + "_"

        + df["Motorista"].astype(str)

        + "_"

        + df["Tipo de Veículo"].astype(str)

    )

    df_unico = df.drop_duplicates(
