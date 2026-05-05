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
        role TEXT,
        nome TEXT,
        fc_max INTEGER,
        fc_repouso INTEGER,
        dias_treino TEXT,
        dia_longo INTEGER,
        volume_horas REAL
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
        duracao REAL,
        descricao TEXT,
        status TEXT
    )
    """)

    # ✅ Criar admin apenas se não existir
    c.execute("SELECT * FROM users WHERE username=?", ("Treller2026",))
    admin = c.fetchone()

    if not admin:
        c.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """, ("Treller2026", "trail2026", "admin"))

    conn.commit()
    conn.close()
