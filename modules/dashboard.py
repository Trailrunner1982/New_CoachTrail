import streamlit as st
from database import get_conn
from engine import calcular_readiness, gerar_treino, calcular_load, calcular_preparation
from datetime import date


def render_dashboard(user_id):

    st.title("Dashboard Diário")

    conn = get_conn()
    c = conn.cursor()

    hoje = date.today().isoformat()

    # =========================
    # CHECK-IN
    # =========================
    st.subheader("Check-in Diário")

    rpe = st.slider("RPE ontem", 1, 10, 5)
    sleep = st.slider("Qualidade do sono", 1, 10, 7)
    fatigue = st.slider("Fadiga", 1, 10, 5)

    if st.button("Gerar Treino Hoje"):

        readiness, status = calcular_readiness(rpe, sleep, fatigue)

        treino = gerar_treino(readiness)

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
    # OUTPUT
    # =========================
    if "treino" in st.session_state:

        st.subheader("Hoje")

        st.metric("Readiness", st.session_state["readiness"])

        st.info(st.session_state["status"])

        treino = st.session_state["treino"]

        st.success(f"""
Tipo: {treino['type']}

{treino['desc']}
""")

        if st.button("✔ Concluir treino"):

            c.execute("""
            UPDATE workouts
            SET completed=1
            WHERE user_id=? AND date=?
            """, (user_id, hoje))

            conn.commit()
            st.success("Treino registado")

    # =========================
    # PROGRESSO
    # =========================
    prep = calcular_preparation(conn, user_id)

    st.subheader("Preparação")

    st.progress(prep / 100)
    st.write(f"{prep}% preparado")
