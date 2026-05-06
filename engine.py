from datetime import date


def readiness_score(hrv, sleep, body, rhr, stress):

    score = (
        hrv * 0.2 +
        sleep * 10 +
        body * 0.5 -
        rhr * 0.3 -
        stress * 2
    )

    score = max(0, min(100, int(score)))

    if score > 80:
        status = "Verde"
    elif score > 50:
        status = "Amarelo"
    else:
        status = "Vermelho"

    return score, status


def gerar_treino(status):

    if status == "Vermelho":
        return "Descanso ativo 30min + mobilidade"

    if status == "Amarelo":
        return "45min Z2 + técnica"

    if status == "Verde":
        return "Intervalos 6x3min Z4 + 2min recuperação"
