from datetime import timedelta
import random


def gerar_treino(volume, tipo):

    if tipo == "easy":
        dist = round(volume * 0.15, 1)
        return {
            "tipo": "Easy Run",
            "cor": "green",
            "descricao": f"""
🏃 Easy Run

Distância: {dist} km  
Duração: {dist*6:.0f} min  
Pace: confortável  

Zona: Z2  

🎯 Recuperação ativa
"""
        }

    if tipo == "tempo":
        return {
            "tipo": "Tempo Run",
            "cor": "yellow",
            "descricao": """
🏃 Tempo Run

Aquecimento: 15 min Z2  
Bloco: 20 min Z3-Z4  
Cooldown: 10 min  

🎯 Limiar anaeróbico
"""
        }

    if tipo == "intervalo":
        return {
            "tipo": "Intervalos",
            "cor": "red",
            "descricao": """
🏃 Intervalos

Aquecimento: 15 min  
6x (3min Z4 + 2min Z1)  
Cooldown: 10 min  

🎯 VO2max
"""
        }

    if tipo == "longo":
        dist = round(volume * 0.5, 1)
        return {
            "tipo": "Long Run",
            "cor": "purple",
            "descricao": f"""
🏃 Long Run

Distância: {dist} km  
Zona: Z2  

🎯 Resistência
"""
        }

    return {
        "tipo": "Descanso",
        "cor": "gray",
        "descricao": "Descanso total"
    }


def gerar_plano(conn, user_id, data_inicio, data_fim, volume=40):

    plano = []
    d = data_inicio

    semana_tipos = ["easy", "intervalo", "easy", "tempo", "descanso", "easy", "longo"]

    while d <= data_fim:

        for tipo in semana_tipos:

            treino = gerar_treino(volume, tipo)

            plano.append({
                "data": d.strftime("%Y-%m-%d"),
                "tipo": treino["tipo"],
                "descricao": treino["descricao"],
                "cor": treino["cor"]
            })

            d += timedelta(days=1)

        volume *= 1.03

    return plano
