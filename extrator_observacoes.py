# ==========================================
# SIGOT
# EXTRATOR DE OBSERVAÇÕES
# ==========================================

import re


def limpar_texto(texto):
    """
    Remove espaços extras e trata valores nulos.
    """
    if texto is None:
        return ""

    texto = str(texto)
    texto = texto.replace("\r", "\n")
    texto = re.sub(r"\n+", "\n", texto)
    texto = re.sub(r"[ ]+", " ", texto)

    return texto.strip()


# ==========================================
# APRESENTAÇÃO
# ==========================================

PADROES_APRESENTACAO = [

    "MG1",
    "MG2",
    "MG3",
    "MG4",

    "RECUO MG1",
    "RECUO MG2",
    "RECUO MG3",
    "RECUO MG4",

    "COPA MG1",
    "COPA MG2",
    "COPA MG3",
    "COPA MG4",

    "PORTARIA 1",
    "PORTARIA 2",
    "PORTARIA 3",
    "PORTARIA 4",
    "PORTARIA 5",
    "PORTARIA 6",
    "PORTARIA 7",

    "PRÉ PRODUÇÃO FIGURINO",
    "PRE PRODUÇÃO FIGURINO",
    "PRE PRODUCAO FIGURINO",

    "FÁBRICA DE CENÁRIOS",
    "FABRICA DE CENARIOS"

]


def extrair_apresentacao(obs):

    texto = limpar_texto(obs).upper()

    for local in PADROES_APRESENTACAO:

        if local in texto:
            return local

    return ""


# ==========================================
# HORÁRIO
# ==========================================

def extrair_horario(obs):

    texto = limpar_texto(obs)

    horario = re.search(r"\b([01]?\d|2[0-3]):([0-5]\d)\b", texto)

    if horario:
        return horario.group()

    return ""


# ==========================================
# LOCAÇÃO
# ==========================================

PALAVRAS_LOCACAO = [

    "LOCAÇÃO",
    "LOCACAO",
    "LOCAL",

]


def extrair_locacao(obs):

    texto = limpar_texto(obs)

    linhas = texto.split("\n")

    for i, linha in enumerate(linhas):

        linha_maiuscula = linha.upper()

        for palavra in PALAVRAS_LOCACAO:

            if palavra in linha_maiuscula:

                if i + 1 < len(linhas):
                    return linhas[i + 1].strip()

    return ""


# ==========================================
# FUNÇÃO PRINCIPAL
# ==========================================

def interpretar_observacao(obs):

    return {

        "apresentacao": extrair_apresentacao(obs),

        "horario": extrair_horario(obs),

        "locacao": extrair_locacao(obs)

    }
