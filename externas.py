import pandas as pd


def resumo_veiculos(grupo):
    """
    Retorna a quantidade de veículos exatamente como aparecem no Excel.
    """

    contagem = (
        grupo["Tipo de Veículo"]
        .fillna("Não informado")
        .value_counts()
    )

    linhas = []

    for tipo, qtd in contagem.items():
        linhas.append(f"{qtd:02d} {tipo}")

    return linhas


def horario_operacional(grupo):
    """
    Define o horário principal da externa.

    Prioridade:
    1 - Camarim
    2 - Van Passeio
    3 - Menor horário da operação
    """

    grupo = grupo.copy()

    grupo["Data Hora"] = pd.to_datetime(
        grupo["Data Hora"],
        errors="coerce"
    )

    camarim = grupo[
        grupo["Tipo de Veículo"]
        .str.contains("CAMARIM", case=False, na=False)
    ]

    if not camarim.empty:
        return camarim["Data Hora"].min()

    vans = grupo[
        grupo["Tipo de Veículo"]
        .str.contains("VAN PASSEIO", case=False, na=False)
    ]

    if not vans.empty:
        return vans["Data Hora"].min()

    return grupo["Data Hora"].min()
