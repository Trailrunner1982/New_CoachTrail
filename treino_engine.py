from datetime import timedelta


def gerar_plano(data_inicio, data_fim):
    plano = []
    d = data_inicio
    semana = 1

    while d <= data_fim:

        tipo = "Z2"
        desc = f"""
🏃 Endurance

🔹 8-12 km
🔹 60 min
🔹 Zona 2

🎯 Base aeróbica
"""

        if semana % 2 == 0:
            tipo = "Intervalado"
            desc = """
🏃 Intervalado

🔹 10km total
🔹 5x(3min Z4 + 2min Z1)

🎯 VO2max
"""

        plano.append({
            "data": d.strftime("%Y-%m-%d"),
            "tipo": tipo,
            "descricao": desc
        })

        d += timedelta(days=1)
        semana += 1

    return plano
