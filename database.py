import sqlite3

DB = "ultracoach.db"


def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)


def init_db():
    conn = get_conn()
    c = conn.cursor()

    # =====================
    # USERS (LOGIN)
    # =====================
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # =====================
    # PERFIL PESSOAL
    # =====================
    c.execute("""
    CREATE TABLE IF NOT EXISTS perfil (
        user_id INTEGER PRIMARY KEY,
        nome TEXT,
        data_nascimento TEXT,
        altura REAL,
        peso REAL
    )
    """)

    # =====================
    # CONFIG TREINO
    # =====================
    c.execute("""
    CREATE TABLE IF NOT EXISTS treino_config (
        user_id INTEGER PRIMARY KEY,
        dias_treino TEXT,
        dia_longo INTEGER,
        volume_km REAL,
        volume_horas REAL,
        preferencia TEXT
    )
    """)

    # =====================
    # MÉTRICAS DIÁRIAS
    # =====================
    c.execute("""
    CREATE TABLE IF NOT EXISTS metricas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        data TEXT,
        hrv REAL,
        rhr REAL,
        sleep REAL,
        body_battery REAL,
        vo2 REAL
    )
    """)

    # =====================
    # OBJETIVOS
    # =====================
    c.execute("""
    CREATE TABLE IF NOT EXISTS objetivos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        nome TEXT,
        data TEXT,
        distancia REAL,
        dplus REAL,
        tempo_objetivo TEXT,
        prioridade TEXT
    )
    """)

    # =====================
    # PLANO
    # =====================
    c.execute("""
    CREATE TABLE IF NOT EXISTS plano (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        data TEXT,
        tipo TEXT,
        duracao REAL,
        descricao TEXT,
        status TEXT
    )
    """)

    # =====================
    # BIBLIOTECA
    # =====================
    c.execute("""
    CREATE TABLE IF NOT EXISTS biblioteca (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        tipo TEXT,
        link TEXT,
        descricao TEXT
    )
    """)

    # ADMIN DEFAULT
    c.execute("SELECT * FROM users WHERE username=?", ("Treller2026",))
    if not c.fetchone():
        c.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """, ("Treller2026", "trail2026", "admin"))

    conn.commit()
    conn.close()
