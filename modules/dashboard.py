import streamlit as st
from database import get_conn
import datetime


def render_dashboard(user_id):
    st.title("Dashboard")

    conn = get_conn()
    c = conn.cursor()

    hoje = str(datetime.date.today())

    # 🔥 MÉTRICAS HOJE
    c.execute("""
    SELECT hrv, rhr FROM metricas
    WHERE user_id=? AND data=?
    """, (user_id, hoje))
    m = c.fetchone()

    if m:
        hrv, rhr = m
        if hrv > 60:
            estado = "🟢 Pronto para treinar"
        elif hrv > 45:
            estado = "🟡 Treino moderado"
        else:
            estado = "🔴 Recuperação necessária"

        st.metric("Estado", estado)
    else:
        st.warning("Sem métricas hoje")

    # 🔥 TREINO DO DIA
    c.execute("""
    SELECT descricao, status FROM plano
    WHERE user_id=? AND data=?
    """, (user_id, hoje))
    treino = c.fetchone()

    if treino:
        st.subheader("Treino de Hoje")
        st.write(treino[0])

    # 🔥 CONSISTÊNCIA
    c.execute("SELECT COUNT(*) FROM plano WHERE user_id=?", (user_id,))
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM plano WHERE user_id=? AND status='feito'", (user_id,))
    feitos = c.fetchone()[0]

    if total > 0:
        perc = int((feitos / total) * 100)
        st.metric("Consistência", f"{perc}%")
