from datetime import datetime, timedelta


def gerar_plano(data_inicio, data_fim):
    plano = []
    d = data_inicio

    while d <= data_fim:
        plano.append({
            "data": d.strftime("%Y-%m-%d"),
            "tipo": "Z2",
            "descricao": "Treino leve 45min Z2"
        })
        d += timedelta(days=1)

    return plano
