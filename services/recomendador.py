from database import get_conn


def obter_recomendacoes(treino, biofeedback=None):
    conn = get_conn()
    c = conn.cursor()

    recomendacoes = []

    # =====================
    # BASEADO NO TREINO
    # =====================
    if treino["forca"]:
        c.execute("SELECT * FROM biblioteca WHERE tipo='video'")
        vids = c.fetchall()
        if vids:
            recomendacoes.append({
                "tipo": "forca",
                "titulo": vids[0][1],
                "link": vids[0][3],
                "descricao": vids[0][4]
            })

    if treino["tipo"] == "subida":
        c.execute("SELECT * FROM biblioteca WHERE titulo LIKE '%subida%'")
        res = c.fetchall()
        if res:
            recomendacoes.append({
                "tipo": "tecnica",
                "titulo": res[0][1],
                "link": res[0][3],
                "descricao": res[0][4]
            })

    # =====================
    # BASEADO NO BIOFEEDBACK (PDF logic)
    # =====================
    if biofeedback:
        if biofeedback["hrv"] < biofeedback["baseline_hrv"]:
            recomendacoes.append({
                "tipo": "alerta",
                "titulo": "Recuperação recomendada",
                "descricao": "HRV baixo — reduzir intensidade hoje"
            })

        if biofeedback["rhr"] > biofeedback["baseline_rhr"]:
            recomendacoes.append({
                "tipo": "alerta",
                "titulo": "Fadiga detectada",
                "descricao": "RHR elevado — foco em treino leve"
            })

    return recomendacoes
