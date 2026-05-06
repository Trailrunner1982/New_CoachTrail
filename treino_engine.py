from datetime import timedelta


def definir_fase(dias_totais, dia_atual):

    pct = dia_atual / dias_totais

    if pct < 0.4:
        return "base"
    elif pct < 0.75:
        return "build"
    elif pct < 0.9:
        return "peak"
    else:
        return "taper"


def treino_por_fase(volume, fase):

    if fase == "base":
        return [
            ("Easy Run", f"{round(volume*0.2)} km Z2"),
            ("Força", "Treino funcional"),
            ("Easy Run", f"{round(volume*0.15)} km Z2"),
            ("Descanso", ""),
            ("Easy Run", f"{round(volume*0.2)} km Z2"),
            ("Descanso", ""),
            ("Long Run", f"{round(volume*0.45)} km Z2"),
        ]

    if fase == "build":
        return [
            ("Intervalos", "5x3min Z4"),
            ("Easy Run", f"{round(volume*0.15)} km Z2"),
            ("Tempo Run", "20min Z3"),
            ("Descanso", ""),
            ("Easy Run", f"{round(volume*0.2)} km Z2"),
            ("Descanso", ""),
            ("Long Run", f"{round(volume*0.5)} km Z2"),
        ]

    if fase == "peak":
        return [
            ("Intervalos", "VO2max"),
            ("Easy Run", "Z2"),
            ("Tempo Run", "Z3-Z4"),
            ("Descanso", ""),
            ("Easy Run", "Z2"),
            ("Descanso", ""),
            ("Long Run", "Simulação prova"),
        ]

    if fase == "taper":
        return [
            ("Easy Run", "curto Z2"),
            ("Descanso", ""),
            ("Tempo Run", "leve"),
            ("Descanso", ""),
            ("Easy Run", "curto"),
            ("Descanso", ""),
            ("Descanso", ""),
        ]


def gerar_descricao(tipo, detalhe):

    return f"""
🏃 {tipo}

📋 Detalhe:
{detalhe}

🎯 Objetivo:
Treino específico da fase

⚠ Controlar esforço
"""


def gerar_plano_prova(data_inicio, data_prova, volume_inicial=40):

    plano = []
    dias_totais = (data_prova - data_inicio).days
    d = data_inicio
    dia_idx = 0
    volume = volume_inicial

    while d <= data_prova:

        fase = definir_fase(dias_totais, dia_idx)

        semana = treino_por_fase(volume, fase)

        for tipo, detalhe in semana:

            plano.append({
                "data": d.strftime("%Y-%m-%d"),
                "tipo": tipo,
                "descricao": gerar_descricao(tipo, detalhe),
                "fase": fase
            })

            d += timedelta(days=1)
            dia_idx += 1

        # progressão
        if fase in ["base", "build"]:
            volume *= 1.05
        elif fase == "peak":
            volume *= 1.02
        elif fase == "taper":
            volume *= 0.85

    return plano
