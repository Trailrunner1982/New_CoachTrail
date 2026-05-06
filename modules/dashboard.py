import streamlit as st
from database import get_conn
import datetime


def render_dashboard(user_id):
    st.title("Dashboard")

    conn = get_conn()
    c = conn.cursor()

    hoje = str(datetime.date.today())

    # =========================
    # MÉTRICAS
    # =========================
    c.execute("""
    SELECT hrv, rhr FROM metricas
    WHERE user_id=? AND data=?
    """, (user_id, hoje))
    m = c.fetchone()

    if m:
        hrv, rhr = m

        if hrv > 60:
            estado = "🟢 Pronto"
            cor = "green"
        elif hrv > 45:
            estado = "🟡 Moderado"
            cor = "yellow"
        else:
            estado = "🔴 Recuperação"
            cor = "red"

        st.markdown(f"""
        <div class="card {cor}">
        <h3>Estado</h3>
        <p>{estado}</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Sem métricas hoje")

    # =========================
    # TREINO HOJE
    # =========================
    c.execute("""
    SELECT descricao FROM plano
    WHERE user_id=? AND data=?
    """, (user_id, hoje))
    treino = c.fetchone()

    if treino:
        st.subheader("Treino de Hoje")
        st.markdown(f"""
        <div class="card blue">
        {treino[0]}
        </div>
        """, unsafe_allow_html=True)
