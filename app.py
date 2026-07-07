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
        subset=["Chave Operacional"]
    ).copy()

    # ==================================================
    # CATEGORIA
    # ==================================================

    df_unico["Categoria Operacional"] = (
        df_unico["Tipo de Veículo"]
        .apply(identificar_categoria)
    )

    # ==================================================
    # EXTERNA
    # ==================================================

    df_unico["Externa"] = df_unico.apply(
        identificar_externa,
        axis=1
    )

    # ==================================================
    # DASHBOARD
    # ==================================================

    st.markdown("---")

    total_veiculos = len(df_unico)

    total_externas = len(
        df_unico[
            df_unico["Externa"] == True
        ]
    )

    total_camarins = len(
        df_unico[
            df_unico["Categoria Operacional"]
            == "🎭 CAMARIM"
        ]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🚚 Veículos Reais",
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

    # ==================================================
    # RESUMO
    # ==================================================

    st.markdown("---")

    st.markdown(
        "# 📊 RESUMO POR CATEGORIA"
    )

    resumo = (
        df_unico["Categoria Operacional"]
        .value_counts()
        .reset_index()
    )

    resumo.columns = [
        "Categoria",
        "Quantidade"
    ]

    st.table(resumo)

    # ==================================================
    # BOLETIM
    # ==================================================

    st.markdown("---")

    st.markdown(
        "# 🚚 BOLETIM DE EXTERNAS"
    )

    externas = df_unico[
        df_unico["Externa"] == True
    ]

    grupos = externas.groupby(
        ["OS", "Programa"],
        dropna=False
    )

    texto_boletim = ""

    for (os, programa), grupo in grupos:

        horario = grupo["Data Hora"].min()

        horario_txt = (
            horario.strftime("%H:%M")
            if pd.notnull(horario)
            else "Sem horário"
        )

        observacoes = " ".join(
            grupo["Observações"]
            .fillna("")
            .astype(str)
            .tolist()
        )

        apresentacao = extrair_apresentacao(
            observacoes
        )

        locacao = extrair_locacao(
            observacoes
        )

        texto_boletim += (
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        )

        texto_boletim += (
            f"🎬 {programa}\n\n"
        )

        texto_boletim += (
            f"🆔 OS: {os}\n\n"
        )

        texto_boletim += (
            "🕓 Saída EG\n"
        )

        texto_boletim += (
            f"{horario_txt}\n\n"
        )

        if apresentacao:

            texto_boletim += (
                "🏢 Apresentação\n"
            )

            texto_boletim += (
                f"{apresentacao}\n\n"
            )

        if locacao:

            texto_boletim += (
                "📍 Locação\n"
            )

            texto_boletim += (
                f"{locacao}\n\n"
            )

        texto_boletim += (
            "🚘 Operação\n\n"
        )

        tipos = (
            grupo["Tipo de Veículo"]
            .value_counts()
        )

        total = 0

        for tipo, qtd in tipos.items():

            texto_boletim += (
                f"{qtd:02d} {tipo}\n"
            )

            total += qtd

        texto_boletim += "\n"

        texto_boletim += (
            f"🚚 Total: {total} veículos\n\n"
        )

    st.text(texto_boletim)

    # ==================================================
    # PRÉVIA
    # ==================================================

    st.markdown("---")

    st.subheader(
        "📊 Prévia do Excel"
    )

    st.dataframe(df_unico.head())
