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

    # CAMARIM / FIGURINO

    if (
        "CAMARIM" in tipo
        or "FIGURINO" in tipo
    ):

        return True

    # OBSERVAÇÃO

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
    # CHAVE OPERACIONAL
    # ==============================================

    df["Chave Operacional"] = (

        df["OT"].astype(str)

        + "_"

        + df["Motorista"].astype(str)

        + "_"

        + df["Tipo de Veículo"].astype(str)

    )

    # ==============================================
    # REMOVE DUPLICIDADE
    # ==============================================

    df_unico = df.drop_duplicates(
        subset=["Chave Operacional"]
    )

    # ==============================================
    # CATEGORIA
    # ==============================================

    df_unico["Categoria Operacional"] = (
        df_unico["Tipo de Veículo"]
        .apply(identificar_categoria)
    )

    # ==============================================
    # EXTERNA
    # ==============================================

    df_unico["Externa"] = df_unico.apply(
        identificar_externa,
        axis=1
    )

    # ==============================================
    # DASHBOARD
    # ==============================================

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

    # ==============================================
    # RESUMO
    # ==============================================

    st.markdown("---")

    st.markdown(
        "# 📊 RESUMO POR CATEGORIA"
    )

    resumo = (

        df_unico[
            "Categoria Operacional"
        ]

        .value_counts()

        .reset_index()

    )

    resumo.columns = [
        "Categoria",
        "Quantidade"
    ]

    st.table(resumo)

    # ==============================================
# EXTERNAS
# ==============================================

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

for (os_num, programa), grupo in grupos:

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
    ).upper()

    apresentacao = ""

    for item in [
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
        "PA 20"
    ]:

        if item in observacoes:
            apresentacao = item
            break

    locacao = ""

    for item in [
        "FAZENDA INDIANA",
        "MUSAL",
        "MERCADO SUPERBOM",
        "SUPERBOM",
        "BAR SALETE",
        "ATERRO DO FLAMENGO",
        "TAVARES BASTOS"
    ]:

        if item in observacoes:
            locacao = item
            break

    st.markdown("━━━━━━━━━━━━━━━━━━━━━━")

    st.markdown(
        f"### 🎬 {programa}"
    )

    st.markdown(
        f"**🆔 OS:** {os_num}"
    )

    st.markdown(
        f"**🕓 Saída EG:** {horario_txt}"
    )

    if apresentacao:

        st.markdown(
            f"**🏢 Apresentação:** {apresentacao}"
        )

    if locacao:

        st.markdown(
            f"**📍 Locação:** {locacao}"
        )

    st.markdown("### 🚘 Operação")

    tipos = (
        grupo["Tipo de Veículo"]
        .value_counts()
    )

    total = 0

    for tipo, qtd in tipos.items():

        total += qtd

        st.markdown(
            f"- {qtd:02d} {tipo}"
        )

    st.markdown(
        f"### 🚚 Total: {total} veículos"
    )

    # ==============================================
    # PRÉVIA
    # ==============================================

    st.markdown("---")

    st.subheader(
        "📊 Prévia do Excel"
    )

    st.dataframe(df_unico.head())
