# ==========================================
# SIGOT
# MAPA DE SOLICITANTES
# ==========================================

import streamlit as st
import pandas as pd


def gerar_mapa_solicitante(df):

    st.subheader("🗺️ MAPA DE SOLICITANTES")

    # Verifica se a planilha possui as colunas mínimas
    colunas_necessarias = [
        "OS",
        "Motorista",
        "Passageiro",
        "Data Hora",
        "Placa Veículo"
    ]

    faltando = [
        c for c in colunas_necessarias
        if c not in df.columns
    ]

    if faltando:
        st.error(
            "Esta planilha não possui as colunas necessárias.\n\n"
            f"Colunas ausentes: {', '.join(faltando)}"
        )
        return

    # Corrige data
    df["Data Hora"] = pd.to_datetime(
        df["Data Hora"],
        errors="coerce"
    )

    # Ordena
    df = df.sort_values("Data Hora")

    # Agrupa por motorista
    motoristas = df.groupby("Motorista")

    for motorista, grupo in motoristas:

        st.markdown("---")

        st.markdown(f"## 🚐 {motorista}")

        placa = ""

        if "Placa Veículo" in grupo.columns:
            placa = grupo["Placa Veículo"].iloc[0]

        st.write(f"**Placa:** {placa}")

        if "OS" in grupo.columns:
            st.write(f"**OS:** {grupo['OS'].iloc[0]}")

        tabela = grupo[
            [
                "Data Hora",
                "Passageiro"
            ]
        ].copy()

        tabela["Data Hora"] = tabela["Data Hora"].dt.strftime(
            "%d/%m/%Y %H:%M"
        )

        tabela.columns = [
            "Horário",
            "Passageiro"
        ]

        st.dataframe(
            tabela,
            use_container_width=True
        )

        st.write(f"Total de passageiros: **{len(grupo)}**")
