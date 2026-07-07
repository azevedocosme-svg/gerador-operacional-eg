import re

PADROES_APRESENTACAO = [

    "RECUO MG1",
    "RECUO DO MG1",

    "RECUO MG3",
    "RECUO DO MG3",

    "RECUO MG4",
    "RECUO DO MG4",

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

PALAVRAS_LOCACAO = [

    "FAZENDA INDIANA",

    "MUSAL",

    "MERCADO SUPERBOM",

    "SUPERBOM",

    "BAR SALETE",

    "ATERRO DO FLAMENGO",

    "BOSQUE DA GLORIA",

    "TAVARES BASTOS",

    "CATETE",

    "TIJUCA"
]


def interpretar_observacao(obs):

    texto = str(obs).upper()

    apresentacao = None
    locacao = None

    for item in PADROES_APRESENTACAO:

        if item in texto:
            apresentacao = item
            break

    for item in PALAVRAS_LOCACAO:

        if item in texto:
            locacao = item
            break

    return {
        "apresentacao": apresentacao,
        "locacao": locacao
    }
