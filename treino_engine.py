from datetime import timedelta


def gerar_treino(volume, tipo):

    if tipo == "easy":
        dist = round(volume * 0.15,1)
        pace = "Z2"
        return f"""
🏃 Easy Run

Distância: {dist} km
Duração: ~{dist*6:.0f} min
Zona: {pace}

🎯 Base aeróbica
"""

    if tipo == "intervalo":
        return """
🏃 Intervalos

Aquecimento: 15min Z2
6x (3min Z4 + 2min Z1)
Cooldown: 10min

🎯 VO2max
"""

    if tipo == "tempo":
        return """
🏃 Tempo Run

15min Z2
20min Z3-Z4
10min Z1

🎯 Limiar
"""

    if tipo == "longo":
        dist = round(volume * 0.5,1)
        return f"""
🏃 Long Run

Distância: {dist} km
Zona: Z2

🎯 Resistência
"""

    return "Descanso"


def gerar_plano_prova(data_inicio, data_prova, volume=40):

    plano = []
    d = data_inicio

    semana = ["easy","intervalo","easy","tempo","descanso","easy","longo"]

    while d <= data_prova:

        for tipo in semana:

            plano.append({
                "data": d.isoformat(),
                "tipo": tipo,
                "descricao": gerar_treino(volume, tipo)
            })

            d += timedelta(days=1)

        volume *= 1.03

    return plano
