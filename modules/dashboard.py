import streamlit as st
from database import get_conn
from engine import (
    calcular_readiness,
    gerar_treino_inteligente,
    calcular_load,
    calcular_preparation,
    dias_para_prova,
    aplicar_taper
)
from datetime import date


def render_dashboard(user_id):

    st.title("Dashboard Diário")

    conn = get_conn()
    c = conn.cursor()

    hoje = date.today().isoformat()

    # =========================
    # INFO PROVA
    # =========================
    dias_prova = dias_para_prova(conn, user_id)

    if dias_prova is not None:
        st.info(f"🏁 Faltam {dias_prova} dias para a prova")

    # =========================
    # CHECK-IN
    # =========================
    st.subheader("Check-in Diário")

    rpe = st.slider("RPE ontem", 1, 10, 5)
    sleep = st.slider("Sono", 1, 10, 7)
    fatigue = st.slider("Fadiga", 1, 10, 5)

    if st.button("Gerar treino de hoje"):

        readiness, status = calcular_readiness(rpe, sleep, fatigue)

        treino = gerar_treino_inteligente(conn, user_id, readiness)

        # aplicar taper
        treino = aplicar_taper(treino, dias_prova)

        load = calcular_load(treino["duration"], treino["elevation"])

        # guardar readiness
        c.execute("""
        INSERT INTO readiness (user_id, date, score, status)
        VALUES (?, ?, ?, ?)
        """, (user_id, hoje, readiness, status))

        # guardar treino
        c.execute("""
        INSERT INTO workouts (user_id, date, type, planned_load, completed)
        VALUES (?, ?, ?, ?, 0)
        """, (user_id, hoje, treino["type"], load))

        conn.commit()

        st.session_state["treino"] = treino
        st.session_state["readiness"] = readiness
        st.session_state["status"] = status

    # =========================
    # OUTPUT TREINO
    # =========================
    if "treino" in st.session_state:

        treino = st.session_state["treino"]

        st.subheader("Hoje")

        col1, col2 = st.columns(2)

        col1.metric("Readiness", st.session_state["readiness"])
        col2.metric("Estado", st.session_state["status"])

        st.success(f"""
🏃 {treino['type']}

{treino['desc']}

⏱ Duração: {treino['duration']} min  
⛰ Elevação: {treino['elevation']} m
""")

        # =========================
        # CONFIRMAR TREINO
        # =========================
        rpe_post = st.slider("RPE pós-treino", 1, 10, 5)

        if st.button("✔ Concluir treino"):

            c.execute("""
            UPDATE workouts
            SET completed=1, rpe_post=?
            WHERE user_id=? AND date=?
            """, (rpe_post, user_id, hoje))

            conn.commit()

            st.success("Treino registado")

    # =========================
    # PREPARAÇÃO
    # =========================
    st.subheader("Preparação")

    prep = calcular_preparation(conn, user_id)

    st.progress(prep / 100)
    st.write(f"{prep}% preparado")

    # =========================
    # ALERTAS
    # =========================
    if dias_prova is not None:

        if dias_prova < 7:
            st.warning("⚠ Semana de prova — reduzir carga")

        elif dias_prova < 14:
            st.info("📉 Início do taper")
