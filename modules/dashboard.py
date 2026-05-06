import streamlit as st
from database import get_conn


def render_dashboard(user_id):
    st.title("Dashboard")

    conn = get_conn()
    c = conn.cursor()

    # Plano
    c.execute("SELECT COUNT(*) FROM plano WHERE user_id=?", (user_id,))
    total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM plano WHERE user_id=? AND status='feito'", (user_id,))
    feitos = c.fetchone()[0]

    if total > 0:
        percent = int((feitos / total) * 100)
        st.metric("Consistência", f"{percent}%")

    # Treinos realizados
    c.execute("SELECT COUNT(*) FROM treinos WHERE user_id=?", (user_id,))
    treinos = c.fetchone()[0]

    st.metric("Treinos registados", treinos)
