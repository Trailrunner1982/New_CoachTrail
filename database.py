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

    # READINESS
    c.execute("""
    CREATE TABLE IF NOT EXISTS readiness (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        score INTEGER,
        status TEXT
    )
    """)

    # RACE
    c.execute("""
    CREATE TABLE IF NOT EXISTS race (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        distance_km REAL,
        elevation_m REAL
    )
    """)

    # WORKOUTS (PLANEADO + REAL)
    c.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        type TEXT,
        planned_load REAL,
        actual_load REAL,
        completed INTEGER,
        rpe_post INTEGER,
        notes TEXT
    )
    """)

    conn.commit()
