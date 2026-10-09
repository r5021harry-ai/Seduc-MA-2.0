"""
BioConcurso MA - Módulo de Banco de Dados (db.py)
Gerenciamento de persistência local SQLite para preparação SEDUC-MA / FCC.
Consultas parametrizadas, integridade referencial e estatísticas avançadas.
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple

DATABASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DEFAULT_DB_PATH = os.path.join(DATABASE_DIR, "bioconcurso.db")

INTERVALOS_REVISAO = [1, 3, 7, 14, 30]

def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS questoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        disciplina TEXT NOT NULL,
        assunto TEXT NOT NULL,
        subassunto TEXT DEFAULT '',
        enunciado TEXT NOT NULL,
        alt_a TEXT NOT NULL,
        alt_b TEXT NOT NULL,
        alt_c TEXT NOT NULL,
        alt_d TEXT NOT NULL,
        alt_e TEXT NOT NULL,
        gabarito TEXT NOT NULL CHECK(gabarito IN ('A', 'B', 'C', 'D', 'E')),
        comentario TEXT DEFAULT '',
        dificuldade TEXT DEFAULT 'Média' CHECK(dificuldade IN ('Fácil', 'Média', 'Difícil')),
        banca TEXT DEFAULT 'FCC',
        ano INTEGER,
        fonte TEXT DEFAULT '',
        origem TEXT DEFAULT 'usuario' CHECK(origem IN ('oficial_verificada', 'usuario', 'ia_treino')),
        data_cadastro TEXT NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tentativas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        questao_id INTEGER NOT NULL,
        resposta_escolhida TEXT NOT NULL CHECK(resposta_escolhida IN ('A', 'B', 'C', 'D', 'E')),
        correta INTEGER NOT NULL CHECK(correta IN (0, 1)),
        data_hora TEXT NOT NULL,
        modo TEXT DEFAULT 'treino',
        simulado_id TEXT DEFAULT '',
        FOREIGN KEY (questao_id) REFERENCES questoes(id) ON DELETE CASCADE
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS revisoes_espacadas (
        questao_id INTEGER PRIMARY KEY,
        intervalo_dias INTEGER DEFAULT 1,
        repeticoes INTEGER DEFAULT 0,
        proxima_revisao TEXT NOT NULL,
        ultima_revisao TEXT,
        FOREIGN KEY (questao_id) REFERENCES questoes(id) ON DELETE CASCADE
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessoes_estudo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        disciplina TEXT NOT NULL,
        assunto TEXT DEFAULT '',
        minutos_estudo INTEGER DEFAULT 0,
        questoes_feitas INTEGER DEFAULT 0,
        questoes_acertadas INTEGER DEFAULT 0,
        notas TEXT DEFAULT ''
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS configuracoes (
        chave TEXT PRIMARY KEY,
        valor TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()
