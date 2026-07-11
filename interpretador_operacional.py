"""
===========================================
SIGOT
INTERPRETADOR OPERACIONAL
Versão 1.0
===========================================
"""

import re
import pandas as pd

from extrator_observacoes import extrair_informacoes


# ==========================================
# CLASSE DA OPERAÇÃO
# ==========================================

class OperacaoExterna:

    def __init__(self):

        self.producao = ""

        self.os = ""

        self.externa = False

        self.apresentacao = ""

        self.horario_saida = ""

        self.locacao = ""

        self.deslocamentos = []

        self.observacoes = []

        self.veiculos = []

        self.frentes = []

        self.motoristas = []

        self.prestadores = []


# ==========================================
# INTERPRETADOR
# ==========================================

def interpretar_producao(df):

    operacao = OperacaoExterna()

    if len(df) == 0:
        return operacao

    # -------------------------
    # PRODUÇÃO
    # -------------------------

    operacao.producao = str(
        df.iloc[0]["Programa"]
    )

    operacao.os = str(
        df.iloc[0]["OS"]
    )

    # -------------------------
    # ANALISA LINHA A LINHA
    # -------------------------

    for _, linha in df.iterrows():

        tipo = str(
            linha["Tipo de Veículo"]
        )

        observacao = str(
            linha["Observações"]
        )

        passageiro = str(
            linha["Passageiro"]
        )

        motorista = str(
            linha["Motorista"]
        )

        prestador = str(
            linha["Prestador do veículo"]
        )

        # ----------------------
        # VEÍCULOS
        # ----------------------

        operacao.veiculos.append(tipo)

        if motorista and motorista != "nan":
            operacao.motoristas.append(motorista)

        if prestador and prestador != "nan":
            operacao.prestadores.append(prestador)

        # ----------------------
        # IDENTIFICA EXTERNA
        # ----------------------

        tipo_upper = tipo.upper()

        if (
            "CAMARIM" in tipo_upper
            or "FIGURINO" in tipo_upper
        ):
            operacao.externa = True

        # ----------------------
        # PASSAGEIRO
        # ----------------------

        passageiro_upper = passageiro.upper()

        if "EXTERNA" in passageiro_upper:

            operacao.frentes.append(
                passageiro
            )

        # ----------------------
        # OBSERVAÇÃO
        # ----------------------

        dados = extrair_informacoes(
            observacao
        )

        if dados.get("apresentacao"):

            operacao.apresentacao = dados["apresentacao"]

        if dados.get("saida"):

            operacao.horario_saida = dados["saida"]

        if dados.get("locacao"):

            operacao.locacao = dados["locacao"]

        if dados.get("deslocamentos"):

            operacao.deslocamentos.extend(
                dados["deslocamentos"]
            )

        if observacao not in operacao.observacoes:

            operacao.observacoes.append(
                observacao
            )

    # Remove duplicados

    operacao.veiculos = sorted(
        list(set(operacao.veiculos))
    )

    operacao.motoristas = sorted(
        list(set(operacao.motoristas))
    )

    operacao.prestadores = sorted(
        list(set(operacao.prestadores))
    )

    operacao.frentes = sorted(
        list(set(operacao.frentes))
    )

    return operacao
