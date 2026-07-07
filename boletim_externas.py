import pandas as pd
from collections import Counter

from extrator_observacoes import interpretar_observacao


def gerar_boletim(df):

    externas = df[df["Externa"] == True].copy()

    if externas.empty:
        return ["Nenhuma externa encontrada."]

    externas["Data Hora"] = pd.to_datetime(
        externas["Data Hora"],
        errors="coerce"
    )

    boletim = []

    grupos = externas.groupby(
        ["OS", "Programa"],
        dropna=False
    )

    for (os, programa), grupo in grupos:

        grupo = grupo.sort_values("Data Hora")

        horario = grupo["Data Hora"].min()

        horario_txt = (
            horario.strftime("%H:%M")
            if pd.notnull(horario)
            else "Não informado"
        )

        observacoes = " ".join(
            grupo["Observações"]
            .fillna("")
            .astype(str)
            .tolist()
        )

        info = interpretar_observacao(
            observacoes
        )

        apresentacao = info["apresentacao"]
        locacao = info["locacao"]

        contador = Counter(
            grupo["Tipo de Veículo"]
            .fillna("Não informado")
        )

        total = sum(contador.values())

        boletim.append("━━━━━━━━━━━━━━━━━━━━━━")
        boletim.append("")

        boletim.append(f"🎬 {programa}")
        boletim.append("")

        boletim.append(f"🆔 OS: {os}")
        boletim.append("")

        boletim.append("🕓 Saída EG")
        boletim.append(horario_txt)
        boletim.append("")

        if apresentacao:
            boletim.append("🏢 Apresentação")
            boletim.append(apresentacao)
            boletim.append("")

        if locacao:
            boletim.append("📍 Locação")
            boletim.append(locacao)
            boletim.append("")

        boletim.append("🚘 Operação")
        boletim.append("")

        for veiculo, qtd in sorted(
            contador.items(),
            key=lambda x: x[1],
            reverse=True
        ):

            boletim.append(
                f"{qtd:02d} {veiculo}"
            )

        boletim.append("")
        boletim.append(
            f"🚚 Total: {total} veículos"
        )

        boletim.append("")
        boletim.append("")

    return boletim
