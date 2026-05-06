from datetime import timedelta


def gerar_plano(data_inicio, data_fim):
    plano = []
    d = data_inicio

    while d <= data_fim:

        plano.append({
            "data": d.strftime("%Y-%m-%d"),
            "tipo": "Z2",
            "descricao": f"""
🏃 Treino Endurance

Distância: 8-12km
Duração: 50-70 min
Zona: Z2

🎯 Objetivo:
Desenvolver base aeróbica

⚠ Manter esforço confortável
"""
        })

        d += timedelta(days=1)

    return plano
