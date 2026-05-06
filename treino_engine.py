from datetime import timedelta


def analisar_estado(conn, user_id):

    c = conn.cursor()

    # Consistência
    c.execute("SELECT COUNT(*) FROM plano WHERE user_id=?", (user_id,))
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM plano WHERE user_id=? AND status='feito'", (user_id,))
    feitos = c.fetchone()[0]

    consistencia = feitos / total if total > 0 else 0

    # Métricas (últimos 7 dias)
    c.execute("""
    SELECT AVG(hrv), AVG(rhr)
    FROM metricas
    WHERE user_id=?
    ORDER BY data DESC LIMIT 7
    """, (user_id,))
    m = c.fetchone()

    hrv = m[0] if m[0] else 50
    rhr = m[1] if m[1] else 60

    # Falhas
    c.execute("""
    SELECT COUNT(*) FROM plano
    WHERE user_id=? AND status='falhou'
    """, (user_id,))
    falhas = c.fetchone()[0]

    return consistencia, hrv, rhr, falhas


def ajustar_volume(volume, consistencia):
    if consistencia > 0.8:
        return volume * 1.05
    elif consistencia < 0.5:
        return volume * 0.9
    return volume


def gerar_semana(volume, intensidade_reduzida=False):

    semana = []

    semana.append({
        "tipo": "Endurance",
        "desc": f"""
🏃 Endurance

Distância: {round(volume*0.2)} km
Zona: Z2

🎯 Base aeróbica
"""
    })

    if intensidade_reduzida:
        semana.append({
            "tipo": "Recuperação",
            "desc": """
🏃 Recuperação

Zona: Z1

🎯 Regeneração
"""
        })
    else:
        semana.append({
            "tipo": "Intervalado",
            "desc": """
🏃 Intervalado

5x(3min Z4 + 2min Z1)

🎯 VO2max
"""
        })

    semana.append({
        "tipo": "Longo",
        "desc": f"""
🏃 Longo

Distância: {round(volume*0.5)} km
Zona: Z2

🎯 Resistência
"""
    })

    return semana


def gerar_plano(conn, user_id, data_inicio, data_fim, volume_inicial=40):

    consistencia, hrv, rhr, falhas = analisar_estado(conn, user_id)

    volume = ajustar_volume(volume_inicial, consistencia)

    intensidade_reduzida = False

    if hrv < 45 or rhr > 65:
        intensidade_reduzida = True

    if falhas >= 3:
        intensidade_reduzida = True
        volume *= 0.8

    plano = []
    d = data_inicio

    while d <= data_fim:

        semana = gerar_semana(volume, intensidade_reduzida)

        for treino in semana:

            plano.append({
                "data": d.strftime("%Y-%m-%d"),
                "tipo": treino["tipo"],
                "descricao": treino["desc"]
            })

            d += timedelta(days=1)

        volume *= 1.02  # progressão leve

    return plano
