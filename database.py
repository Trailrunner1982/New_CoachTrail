import sqlite3

DB = "ultracoach.db"


def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)


def init_db():
    conn = get_conn()
    c = conn.cursor()

    # USERS
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # PERFIL
    c.execute("""
    CREATE TABLE IF NOT EXISTS perfil (
        user_id INTEGER PRIMARY KEY,
        nome TEXT,
        data_nascimento TEXT,
        altura REAL
    )
    """)

    # PESO HISTÓRICO
    c.execute("""
    CREATE TABLE IF NOT EXISTS peso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        data TEXT,
        peso REAL
    )
    """)

    # TREINO CONFIG
    c.execute("""
    CREATE TABLE IF NOT EXISTS treino_config (
        user_id INTEGER PRIMARY KEY,
        dias TEXT,
        dia_longo TEXT,
        volume_km REAL,
        pace REAL,
        forca INTEGER,
        forca_dias TEXT
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
        dplus REAL,
        tempo TEXT,
        prioridade TEXT
    )
    """)

    # MÉTRICAS
    c.execute("""
    CREATE TABLE IF NOT EXISTS metricas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        data TEXT,
        hrv REAL,
        rhr REAL,
        sleep REAL,
        body REAL,
        vo2 REAL
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

    # TREINOS REALIZADOS
    c.execute("""
    CREATE TABLE IF NOT EXISTS treinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        data TEXT,
        tipo TEXT,
        distancia REAL,
        duracao REAL,
        pace REAL,
        fc REAL,
        dplus REAL,
        notas TEXT
    )
    """)

    # BIBLIOTECA
    c.execute("""
    CREATE TABLE IF NOT EXISTS biblioteca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        link TEXT,
        descricao TEXT
    )
    """)

    # ADMIN
    c.execute("SELECT * FROM users WHERE username=?", ("Treller2026",))
    if not c.fetchone():
        c.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """, ("Treller2026", "trail2026", "admin"))

    conn.commit()
    conn.close()
