import pandas as pd
from collections import Counter


def gerar_boletim(df):

    externas = df[df["Externa"] == True].copy()

    if externas.empty:
        return ["Nenhuma externa encontrada."]

    # Ordena pelo horário
    externas = externas.sort_values("Data Hora")

    boletim = []

    grupos = externas.groupby(["OS", "Programa"], dropna=False)

    for (os, programa), grupo in grupos:

        horario = pd.to_datetime(grupo["Data Hora"]).min()

        horario = horario.strftime("%H:%M")

        boletim.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        boletim.append("")
        boletim.append(f"🎬 {programa}")
        boletim.append(f"🆔 OS: {os}")
        boletim.append("")
        boletim.append(f"🕓 Horário: {horario}")

        # Local
        endereco = grupo["Localidade + Endereço"].dropna()

        if len(endereco):

            boletim.append("")
            boletim.append("📍 Local")

            boletim.append(endereco.iloc[0])

        boletim.append("")
        boletim.append("🚘 Operação")

        contador = Counter(grupo["Tipo de Veículo"])

        total = 0

        for veiculo, qtd in sorted(contador.items()):

            boletim.append(f"{qtd:02d} {veiculo}")

            total += qtd

        boletim.append("")
        boletim.append(f"🚚 Total: {total} veículos")
        boletim.append("")

    return boletim
