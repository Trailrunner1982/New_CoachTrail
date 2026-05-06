import streamlit as st
from database import get_conn


def render_objetivos(user_id):
    st.title("Objetivos")

    conn = get_conn()
    c = conn.cursor()

    st.subheader("Nova Prova")

    nome = st.text_input("Nome")
    data = st.date_input("Data")
    dist = st.number_input("Distância (km)")
    dplus = st.number_input("D+")
    prioridade = st.selectbox("Prioridade", ["A", "B", "C"])

    if st.button("Adicionar Prova", use_container_width=True):
        c.execute("""
        INSERT INTO objetivos
        (user_id, nome, data, distancia, dplus, prioridade)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, nome, str(data), dist, dplus, prioridade))
        conn.commit()
        st.success("Adicionado")

    st.divider()

    st.subheader("Objetivos existentes")

    c.execute("SELECT * FROM objetivos WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    for r in rows:
        st.write(f"{r[2]} | {r[3]} | {r[6]}")
