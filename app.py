import streamlit as st
import pandas as pd
import re

# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.set_page_config(
    page_title="SIGOT",
    layout="wide"
)

# ==================================================
# TÍTULO
# ==================================================

st.title("🚀 SIGOT")
st.subheader("Sistema Inteligente de Gestão Operacional de Transportes")

# ==================================================
# IMPORTAÇÃO
# ==================================================

arquivo = st.file_uploader(
    "📥 Importar Relatório Excel",
    type=["xlsx"]
)

# ==================================================
# FUNÇÕES
# ==================================================

def limpar_nome_programa(nome):

    if pd.isna(nome):
        return "NÃO IDENTIFICADO"

    nome = str(nome)

    partes = nome.split("-")

    if len(partes) >= 3:
        nome_limpo = partes[2]
    else:
        nome_limpo = nome

    nome_limpo = nome_limpo.split("/")[0]

    return nome_limpo.strip().upper()


def obter_os(nome):

    if pd.isna(nome):
        return "-"

    nome = str(nome)

    partes = nome.split("-")

    if len(partes) > 0:
        return partes[0].strip()

    return "-"


def extrair_locacao(obs, endereco):

    texto = f"{obs} {endereco}"

    if pd.isna(texto):
        return "Locação não identificada"

    texto = str(texto)

    palavras_chave = [
        "FAZENDA",
        "PRAIA",
        "ESTRADA",
        "AVENIDA",
        "RUA",
        "HOTEL",
        "SÍTIO",
        "SITIO",
        "HARAS",
        "GALPÃO",
        "GALPAO",
        "STUDIO",
        "EXTERNA",
        "LOCAÇÃO",
        "LOCACAO"
    ]

    for palavra in palavras_chave:

        if palavra in texto.upper():
            return texto[:150]

    return "Locação não identificada"


# ==================================================
# PROCESSAMENTO
# ==================================================

if arquivo:

    df = pd.read_excel(arquivo)

    st.success("✅ Arquivo carregado com sucesso")

    # ==================================================
    # COLUNAS
    # ==================================================

    st.markdown("## 📋 COLUNAS ENCONTRADAS")
    st.write(df.columns.tolist())

    # ==================================================
    # CONSOLIDAÇÃO POR OT
    # ==================================================

    df_consolidado = df.drop_duplicates(subset=["OT"])

    total_veiculos = len(df_consolidado)

    # ==================================================
    # EXTERNAS
    # ==================================================

    palavras_externa = [
        "CAMARIM",
        "FIGURINO",
        "FURGÃO",
        "FURGAO",
        "PICK",
        "BLINDADO"
    ]

    mask_externa = df_consolidado["Tipo de Veículo"].astype(str).str.upper().str.contains(
        "|".join(palavras_externa),
        na=False
    )

    externas = df_consolidado[mask_externa]

    total_externas = externas["Programa"].nunique()

    # ==================================================
    # CAMARIM
    # ==================================================

    mask_camarim = df_consolidado["Tipo de Veículo"].astype(str).str.upper().str.contains(
        "CAMARIM",
        na=False
    )

    total_camarim = len(df_consolidado[mask_camarim])

    # ==================================================
    # FIGURINO
    # ==================================================

    mask_figurino = df_consolidado["Tipo de Veículo"].astype(str).str.upper().str.contains(
        "FIGURINO",
        na=False
    )

    total_figurino = len(df_consolidado[mask_figurino])

    # ==================================================
    # PRESTADORES
    # ==================================================

    prestadores = (
        df_consolidado["Prestador do Motorista"]
        .value_counts()
        .reset_index()
    )

    prestadores.columns = ["Prestador", "Quantidade"]

    # ==================================================
    # ALERTAS
    # ==================================================

    sem_placa = df_consolidado["Placa Veículo"].isna().sum()

    sem_telefone = df_consolidado["Telefone Motorista"].isna().sum()

    # ==================================================
    # ISO
    # ==================================================

    iso = 0

    iso += total_externas * 5
    iso += total_camarim * 8
    iso += total_figurino * 6

    if iso <= 30:
        status_iso = "🟢 Operação Estável"

    elif iso <= 60:
        status_iso = "🟡 Operação Sensível"

    else:
        status_iso = "🔴 Operação Crítica"

    # ==================================================
    # DASHBOARD
    # ==================================================

    st.markdown("---")

    st.markdown("# 📊 DASHBOARD OPERACIONAL")

    st.success(status_iso)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🚚 Veículos", total_veiculos)
    col2.metric("🎬 Externas", total_externas)
    col3.metric("🎭 Camarins", total_camarim)
    col4.metric("👗 Figurinos", total_figurino)

    st.metric("📈 ISO", iso)

    # ==================================================
    # ALERTAS
    # ==================================================

    st.markdown("---")

    st.markdown("# ⚠️ ALERTAS OPERACIONAIS")

    st.write(f"⚠️ Veículos sem placa: {sem_placa}")
    st.write(f"⚠️ Motoristas sem telefone: {sem_telefone}")

    # ==================================================
    # PRESTADORES
    # ==================================================

    st.markdown("---")

    st.markdown("# 🚛 PRESTADORES")

    st.table(prestadores)

    # ==================================================
    # BOLETIM EXTERNAS
    # ==================================================

    st.markdown("---")

    st.markdown("# 🚚 BOLETIM EXTERNAS")

    for programa in externas["Programa"].dropna().unique():

        grupo = externas[externas["Programa"] == programa]

        programa_limpo = limpar_nome_programa(programa)

        os = obter_os(programa)

        horario = pd.to_datetime(
            grupo["Data Hora"],
            errors="coerce",
            dayfirst=True
        ).min()

        if pd.isna(horario):
            horario_formatado = "Não informado"
        else:
            horario_formatado = horario.strftime("%d/%m/%Y %H:%M")

        total_operacao = len(grupo)

        obs = grupo["Observações"].astype(str).iloc[0]

        endereco = grupo["Localidade + Endereço"].astype(str).iloc[0]

        locacao = extrair_locacao(obs, endereco)

        st.markdown("━━━━━━━━━━━━━━━━━━━━━━")

        st.markdown(f"## 🎬 {programa_limpo}")

        st.markdown(f"🆔 OS: {os}")

        st.markdown(f"📍 {locacao}")

        st.markdown(f"⏰ Início: {horario_formatado}")

        st.markdown(f"🚘 Total da operação: {total_operacao}")

        tipos = grupo["Tipo de Veículo"].value_counts()

        for tipo, qtd in tipos.items():
            st.write(f"🚘 {qtd:02d} {tipo}")
