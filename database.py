import sqlite3


def get_conn():
    return sqlite3.connect("ultra.db", check_same_thread=False)


def init_db():
    conn = get_conn()
    c = conn.cursor()

    # USERS
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # PERFIL
    c.execute("""
    CREATE TABLE IF NOT EXISTS perfil (
        user_id INTEGER PRIMARY KEY,
        nome TEXT,
        nascimento TEXT,
        altura REAL,
        peso REAL,
        fc_max INTEGER,
        fc_repouso INTEGER
    )
    """)

    # PESO HISTORICO
    c.execute("""
    CREATE TABLE IF NOT EXISTS peso_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        data TEXT,
        peso REAL
    )
    """)

    # TREINOS REALIZADOS
    c.execute("""
    CREATE TABLE IF NOT EXISTS treinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        data TEXT,
        tipo TEXT,
        distancia REAL,
        duracao TEXT,
        pace REAL,
        altimetria REAL,
        fc_media INTEGER,
        fc_max INTEGER,
        rpe INTEGER,
        notas TEXT
    )
    """)

    # MÉTRICAS
    c.execute("""
    CREATE TABLE IF NOT EXISTS metricas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        data TEXT,
        hrv REAL,
        rhr INTEGER,
        sleep REAL,
        body REAL
    )
    """)

    # OBJETIVOS
    c.execute("""
    CREATE TABLE IF NOT EXISTS objetivos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        nome TEXT,
        data TEXT,
        distancia REAL,
        altimetria REAL,
        prioridade TEXT
    )
    """)

    # PLANO
    c.execute("""
    CREATE TABLE IF NOT EXISTS plano (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        data TEXT,
        tipo TEXT,
        descricao TEXT,
        status TEXT
    )
    """)

    conn.commit()
