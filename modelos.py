"""
=========================================
SIGOT - MODELOS DE DADOS
=========================================

Este arquivo define as estruturas principais
utilizadas pelo Interpretador Operacional.

Toda a inteligência do SIGOT trabalhará
sobre estes objetos e não diretamente
sobre o DataFrame do Excel.
"""

from dataclasses import dataclass, field
from typing import List


# ==========================================================
# VEÍCULO
# ==========================================================

@dataclass
class Veiculo:
    os: str = ""
    ot: str = ""

    tipo: str = ""

    motorista: str = ""
    telefone: str = ""

    placa: str = ""

    prestador_veiculo: str = ""
    prestador_motorista: str = ""

    passageiro: str = ""

    observacao: str = ""

    localidade: str = ""

    data_hora: str = ""

    status: str = ""

    viagem: str = ""


# ==========================================================
# FRENTE DE OPERAÇÃO
# ==========================================================

@dataclass
class Frente:

    nome: str = ""

    apresentacao: str = ""

    horario_saida: str = ""

    locacao: str = ""

    roteiro: List[str] = field(default_factory=list)

    observacoes: List[str] = field(default_factory=list)

    veiculos: List[Veiculo] = field(default_factory=list)


# ==========================================================
# OPERAÇÃO EXTERNA
# ==========================================================

@dataclass
class OperacaoExterna:

    producao: str = ""

    os: str = ""

    externa: bool = False

    apresentacao: str = ""

    horario_saida: str = ""

    locacao_principal: str = ""

    frentes: List[Frente] = field(default_factory=list)

    veiculos: List[Veiculo] = field(default_factory=list)

    observacoes: List[str] = field(default_factory=list)

    deslocamentos: List[str] = field(default_factory=list)

    evidencias: List[str] = field(default_factory=list)

    pontuacao: int = 0
