import sqlite3

DB = "ultracoach.db"

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        role TEXT,
        nome TEXT,
        fc_max INTEGER,
        fc_repouso INTEGER,
        dias_treino TEXT,
        dia_longo INTEGER,
        volume_horas REAL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS objetivos (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        nome TEXT,
        data TEXT,
        distancia REAL,
        dplus REAL,
        prioridade TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS plano (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        data TEXT,
        tipo TEXT,
        duracao REAL,
        descricao TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
