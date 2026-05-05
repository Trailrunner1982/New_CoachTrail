from datetime import datetime, timedelta

# =========================
# UTILIDADES
# =========================

def calcular_num_semanas(data_objetivo):
    hoje = datetime.today()
    alvo = datetime.fromisoformat(str(data_objetivo))
    dias = (alvo - hoje).days
    return max(1, dias // 7)


def media_ultimas_semanas(historico):
    if not historico:
        return 0
    return sum(historico) / len(historico)


# =========================
# VALIDAÇÃO
# =========================

def validar_objetivo(user, objetivo):
    avisos = []

    dias = len(user["dias_treino"])
    distancia = objetivo["distancia"]

    if dias < 3 and distancia >= 40:
        avisos.append("Poucos dias de treino para esta distância")

    if user["volume_atual_horas"] < 3:
        avisos.append("Volume semanal atual muito baixo")

    return avisos


# =========================
# VOLUME
# =========================

def calcular_volume_base(historico, user):
    if historico:
        return media_ultimas_semanas(historico)
    return user["volume_atual_horas"]


def calcular_volume_semana(base, semana_idx):
    # deload
    if semana_idx % 4 == 3:
        return base * 0.7

    aumento = (semana_idx // 2) * 0.05
    return base * (1 + aumento)


# =========================
# DISTRIBUIÇÃO
# =========================

def distribuir_treinos(user, volume, semana_idx):
    dias = user["dias_treino"]
    n = len(dias)

    if n == 2:
        tipos = ["longo", "intensidade"]
    elif n <= 4:
        tipos = ["longo", "subida", "facil", "intensidade"][:n]
    else:
        tipos = ["longo", "subida", "facil", "facil", "intensidade"][:n]

    treinos = []

    for i, dia in enumerate(dias):
        tipo = tipos[i % len(tipos)]
        treino = gerar_treino(user, tipo, volume, dia)
        treinos.append(treino)

    treinos = adicionar_forca(treinos)

    return treinos


# =========================
# TREINOS
# =========================

def gerar_treino(user, tipo, volume, dia):
    duracao_total_horas = 0
    zonas = []
    dplus = 0
    descricao = ""

    if tipo == "longo":
        duracao_total_horas = volume * 0.4
        minutos = int(duracao_total_horas * 60)

        zonas = [
            ("Z1", 20),
            ("Z2", minutos - 20)
        ]

        dplus = int(duracao_total_horas * 400)
        descricao = "Treino longo aeróbico"

    elif tipo == "subida":
        duracao_total_horas = volume * 0.2
        minutos = int(duracao_total_horas * 60)

        zonas = [
            ("Z2", minutos)
        ]

        dplus = int(duracao_total_horas * 600)
        descricao = "Treino de subida"

    elif tipo == "intensidade":
        duracao_total_horas = volume * 0.2

        zonas = [
            ("Z1", 15),
            ("Z3", 20),
            ("Z1", 10)
        ]

        dplus = 100
        descricao = "Treino de intensidade"

    else:  # facil
        duracao_total_horas = volume * 0.2
        minutos = int(duracao_total_horas * 60)

        zonas = [
            ("Z1", minutos)
        ]

        dplus = 50
        descricao = "Treino fácil"

    return {
        "dia": dia,
        "tipo": tipo,
        "duracao_horas": round(duracao_total_horas, 2),
        "zonas": zonas,
        "dplus": dplus,
        "descricao": descricao,
        "forca": False
    }


# =========================
# FORÇA
# =========================

def adicionar_forca(treinos):
    count = 0

    for treino in treinos:
        if treino["tipo"] in ["facil", "subida"] and count < 2:
            treino["forca"] = True
            count += 1

    return treinos


# =========================
# GERAÇÃO SEMANA
# =========================

def gerar_semana(user, objetivo, semana_idx, total_semanas, base):
    volume = calcular_volume_semana(base, semana_idx)

    treinos = distribuir_treinos(user, volume, semana_idx)

    return {
        "semana": semana_idx + 1,
        "volume": round(volume, 2),
        "treinos": treinos
    }


# =========================
# MOTOR PRINCIPAL
# =========================

def gerar_plano(user, objetivo, historico=[]):
    avisos = validar_objetivo(user, objetivo)

    semanas = calcular_num_semanas(objetivo["data"])

    volume_base = calcular_volume_base(historico, user)

    plano = []

    for semana_idx in range(semanas):
        semana = gerar_semana(
            user,
            objetivo,
            semana_idx,
            semanas,
            volume_base
        )
        plano.append(semana)

    return {
        "plano": plano,
        "avisos": avisos
    }


# =========================
# ADAPTAÇÃO (PRONTO PARA USO FUTURO)
# =========================

def ajustar_plano(plano, biofeedback, falhas):
    if falhas >= 3:
        return reduzir_volume(plano)

    if tendencia_fadiga(biofeedback):
        return reduzir_intensidade(plano)

    return plano


def tendencia_fadiga(bio):
    if len(bio) < 3:
        return False

    hrv_down = all(b["hrv"] < bio[0]["hrv"] for b in bio[-3:])
    rhr_up = all(b["rhr"] > bio[0]["rhr"] for b in bio[-3:])

    return hrv_down and rhr_up


def reduzir_volume(plano):
    for semana in plano:
        semana["volume"] *= 0.8
    return plano


def reduzir_intensidade(plano):
    for semana in plano:
        for t in semana["treinos"]:
            if t["tipo"] == "intensidade":
                t["tipo"] = "facil"
    return plano
