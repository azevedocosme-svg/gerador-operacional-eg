import pandas as pd


def gerar_boletim_executivo(df):

    externas = df[df["Externa"] == True].copy()

    saida = []

    grupos = externas.groupby(
        "Programa",
        dropna=False
    )

    for programa, grupo in grupos:

        grupo = grupo.sort_values(
            "Data Hora"
        )

        horario = grupo[
            "Data Hora"
        ].min()

        horario_txt = (
            horario.strftime("%H:%M")
            if pd.notnull(horario)
            else "-"
        )

        os_num = str(programa).split(
            "-"
        )[0].strip()

        nome = str(programa)

        if " - " in nome:

            partes = nome.split(" - ")

            if len(partes) >= 3:

                nome = partes[2].split("/")[0]

        observacoes = " ".join(
            grupo["Observações"]
            .fillna("")
            .astype(str)
            .tolist()
        ).upper()

        apresentacao = ""

        locais_apresentacao = [
            "PORTARIA 1",
            "PORTARIA 2",
            "PORTARIA 3",
            "PORTARIA 4",
            "COPA MG1",
            "COPA MG3",
            "RECUO MG1",
            "RECUO MG3"
        ]

        for item in locais_apresentacao:

            if item in observacoes:

                apresentacao = item

                break

        locacao = ""

        locais = [
            "FAZENDA INDIANA",
            "MUSAL",
            "MERCADO SUPERBOM",
            "BAR SALETE",
            "ATERRO DO FLAMENGO",
            "TAVARES BASTOS"
        ]

        for item in locais:

            if item in observacoes:

                locacao = item

                break

        saida.append("")
        saida.append("━━━━━━━━━━━━━━━━━━━━━━")
        saida.append("")
        saida.append(f"🎬 {nome}")
        saida.append("")
        saida.append(f"🆔 OS: {os_num}")
        saida.append("")
        saida.append("🕓 Saída EG")
        saida.append(horario_txt)
        saida.append("")

        if apresentacao:

            saida.append("🏢 Apresentação")
            saida.append(apresentacao)
            saida.append("")

        if locacao:

            saida.append("📍 Locação")
            saida.append(locacao)
            saida.append("")

        saida.append("🚘 Operação")
        saida.append("")

        tipos = (
            grupo["Tipo de Veículo"]
            .value_counts()
        )

        total = 0

        for tipo, qtd in tipos.items():

            total += qtd

            saida.append(
                f"{qtd:02d} {tipo}"
            )

        saida.append("")
        saida.append(
            f"🚚 Total: {total} veículos"
        )

    return saida
