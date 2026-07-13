"""
==========================================================
SIGOT - INTERPRETADOR OPERACIONAL
Versão 2.0
==========================================================

Responsável por transformar uma planilha Excel em
objetos OperacaoExterna.

Fluxo:

Excel
    ↓
DataFrame
    ↓
InterpretadorOperacional
    ↓
OperacaoExterna
    ↓
Boletim
Dashboard
Banco
Caravanas

Autor: Projeto SIGOT
"""

from collections import defaultdict
from typing import List

import pandas as pd

from modelos import (
    OperacaoExterna,
    Veiculo,
    Frente
)

from extrator_observacoes import extrair_informacoes

from regras_operacionais import (
    TIPOS_CAMARIM,
    TIPOS_FIGURINO,
    TIPOS_VANS,
    TIPOS_FURGOES,
    TIPOS_KIA
)


class InterpretadorOperacional:
    """
    Classe principal do SIGOT.

    Recebe um DataFrame do Excel e devolve
    uma lista de OperacaoExterna.
    """

    def __init__(self):

        pass

    # =====================================================
    # MÉTODO PRINCIPAL
    # =====================================================

    def interpretar_dataframe(
        self,
        df: pd.DataFrame
    ) -> List[OperacaoExterna]:

        if df.empty:
            return []

        if "Programa" not in df.columns:
            raise Exception(
                "Coluna 'Programa' não encontrada."
            )

        operacoes = []

        grupos = df.groupby("Programa")

        for producao, dados in grupos:

            operacao = self.interpretar_producao(
                producao,
                dados
            )

            if operacao is not None:
                operacoes.append(operacao)

        return operacoes

    # =====================================================
    # INTERPRETAR PRODUÇÃO
    # =====================================================

    def interpretar_producao(
        self,
        producao: str,
        df: pd.DataFrame
    ) -> OperacaoExterna:

        operacao = OperacaoExterna()

        operacao.producao = str(producao)

        # continua no próximo bloco...
