from datetime import date


def calcular_readiness(rpe, sleep, fatigue):

    score = 100 - (fatigue * 15) - (rpe * 10) + (sleep * 10)
    score = max(0, min(100, score))

    if score > 80:
        status = "Alta"
    elif score >= 50:
        status = "Moderada"
    else:
        status = "Baixa"

    return score, status


# =========================
# FADIGA ACUMULADA
# =========================
def calcular_fadiga(conn, user_id):

    c = conn.cursor()

    c.execute("""
    SELECT rpe_post FROM workouts
    WHERE user_id=? AND rpe_post IS NOT NULL
    ORDER BY date DESC LIMIT 3
    """, (user_id,))
    rpes = [r[0] for r in c.fetchall()]

    c.execute("""
    SELECT planned_load FROM workouts
    WHERE user_id=?
    ORDER BY date DESC LIMIT 3
    """, (user_id,))
    loads = [r[0] for r in c.fetchall()]

    if not rpes:
        return 0

    fatigue = (sum(rpes)/len(rpes)) + (sum(loads)/len(loads))/100

    return fatigue


# =========================
# DETETAR FALHAS
# =========================
def detectar_falhas(conn, user_id):

    c = conn.cursor()

    c.execute("""
    SELECT completed FROM workouts
    WHERE user_id=?
    ORDER BY date DESC LIMIT 3
    """, (user_id,))

    rows = c.fetchall()

    falhas = sum(1 for r in rows if r[0] == 0)

    return falhas


# =========================
# GERAR TREINO INTELIGENTE
# =========================
def gerar_treino_inteligente(conn, user_id, readiness):

    fatigue = calcular_fadiga(conn, user_id)
    falhas = detectar_falhas(conn, user_id)

    ajuste_volume = 1.0

    # falhas
    if falhas == 2:
        ajuste_volume *= 0.9
    elif falhas >= 3:
        return {
            "type": "Recuperação Total",
            "desc": "Descanso + mobilidade",
            "duration": 30,
            "elevation": 0
        }

    # fadiga
    if fatigue > 8:
        return {
            "type": "Recuperação",
            "desc": "40min Z1",
            "duration": 40,
            "elevation": 100
        }

    # readiness
    if readiness < 50:
        return {
            "type": "Leve",
            "desc": "40min Z1-Z2",
            "duration": int(40 * ajuste_volume),
            "elevation": 200
        }

    elif readiness < 80:
        return {
            "type": "Endurance",
            "desc": "60min Z2",
            "duration": int(60 * ajuste_volume),
            "elevation": 300
        }

    else:
        return {
            "type": "Qualidade",
            "desc": "Intervalos Z4",
            "duration": int(70 * ajuste_volume),
            "elevation": 400
        }


# =========================
# LOAD TRAIL
# =========================
def calcular_load(duration, elevation):
    return duration * (1 + elevation / 1000)


# =========================
# PREPARAÇÃO
# =========================
def calcular_preparation(conn, user_id):

    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM workouts WHERE user_id=?", (user_id,))
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM workouts WHERE user_id=? AND completed=1", (user_id,))
    done = c.fetchone()[0]

    consistency = done / total if total else 0

    prep = int((consistency * 0.4 + consistency * 0.3 + consistency * 0.3) * 100)

    return prep
    from datetime import date


def dias_para_prova(conn, user_id):

    c = conn.cursor()

    c.execute("""
    SELECT date FROM race
    WHERE user_id=?
    ORDER BY date LIMIT 1
    """, (user_id,))

    row = c.fetchone()

    if not row:
        return None

    prova = date.fromisoformat(row[0])
    hoje = date.today()

    return (prova - hoje).days


def aplicar_taper(treino, dias_prova):

    if dias_prova is None:
        return treino

    # taper leve
    if dias_prova <= 14 and dias_prova > 7:
        treino["duration"] = int(treino["duration"] * 0.8)

    # taper forte
    elif dias_prova <= 7:
        treino["duration"] = int(treino["duration"] * 0.6)
        treino["desc"] = "Treino leve + ativação"

    return treino
