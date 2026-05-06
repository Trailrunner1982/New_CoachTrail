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
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # ADMIN DEFAULT
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        c.execute("""
        INSERT INTO users (username, password, role)
        VALUES ('admin', 'admin123', 'admin')
        """)

    # PERFIL
    c.execute("""
    CREATE TABLE IF NOT EXISTS perfil (
        user_id INTEGER,
        nome TEXT,
        nascimento TEXT,
        altura REAL,
        peso REAL,
        fc_max INTEGER
    )
    """)

    # READINESS
    c.execute("""
    CREATE TABLE IF NOT EXISTS readiness (
        user_id INTEGER,
        date TEXT,
        score INTEGER,
        status TEXT
    )
    """)

    # WORKOUTS
    c.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        user_id INTEGER,
        date TEXT,
        type TEXT,
        planned_load REAL,
        actual_load REAL,
        completed INTEGER,
        rpe_post INTEGER
    )
    """)

    # OBJECTIVOS
    c.execute("""
    CREATE TABLE IF NOT EXISTS objetivos (
        user_id INTEGER,
        nome TEXT,
        data TEXT,
        distancia REAL,
        elevacao REAL,
        prioridade TEXT
    )
    """)

    conn.commit()
