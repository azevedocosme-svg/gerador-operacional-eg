# ==================================================
# IDENTIFICA CATEGORIA OPERACIONAL
# ==================================================

def identificar_categoria(tipo_veiculo):

    tipo_veiculo = str(tipo_veiculo).upper()

    for categoria, palavras in CATEGORIAS.items():

        for palavra in palavras:

            if palavra.upper() in tipo_veiculo:

                return categoria

    return "❓ OUTROS"
