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

    return int(score), status


def calcular_load(duration_min, elevation):

    return duration_min * (1 + elevation / 1000)


def gerar_treino(readiness):

    if readiness < 50:
        return {
            "type": "Recuperação",
            "desc": "30-40min Z1 + mobilidade",
            "duration": 40,
            "elevation": 100
        }

    elif readiness < 80:
        return {
            "type": "Endurance",
            "desc": "60min Z2",
            "duration": 60,
            "elevation": 300
        }

    else:
        return {
            "type": "Qualidade",
            "desc": "6x3min Z4 + 2min rec",
            "duration": 70,
            "elevation": 400
        }


def calcular_preparation(conn, user_id):

    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM workouts WHERE user_id=?", (user_id,))
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM workouts WHERE user_id=? AND completed=1", (user_id,))
    done = c.fetchone()[0]

    consistency = done / total if total else 0

    preparation = int((consistency * 0.4 + consistency * 0.3 + consistency * 0.3) * 100)

    return preparation
