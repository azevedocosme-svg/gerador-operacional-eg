# ==========================================
# SIGOT
# BANCO DE DADOS SQLITE
# ==========================================

import sqlite3


def conectar():

    conn = sqlite3.connect("sigot.db")

    return conn


def criar_tabelas():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS operacoes (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        os TEXT,

        ot TEXT,

        codigo_ot TEXT,

        programa TEXT,

        tipo_veiculo TEXT,

        motorista TEXT,

        telefone TEXT,

        placa TEXT,

        passageiro TEXT,

        observacoes TEXT,

        origem TEXT,

        data_hora TEXT,

        destino TEXT,

        data_hora2 TEXT,

        prestador TEXT,

        status TEXT,

        operacao TEXT,

        viagem TEXT

    )

    """)

    conn.commit()

    conn.close()


def inserir_operacao(dados):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO operacoes(

        os,
        ot,
        codigo_ot,
        programa,
        tipo_veiculo,
        motorista,
        telefone,
        placa,
        passageiro,
        observacoes,
        origem,
        data_hora,
        destino,
        data_hora2,
        prestador,
        status,
        operacao,
        viagem

    )

    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

    """, dados)

    conn.commit()

    conn.close()


def total_operacoes():

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM operacoes")

    total = cursor.fetchone()[0]

    conn.close()

    return total
