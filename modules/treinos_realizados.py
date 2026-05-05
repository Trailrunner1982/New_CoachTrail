import streamlit as st
from database import get_conn
from datetime import date


def render_treinos(user_id):
    st.header("Treinos Realizados")

    data = st.date_input("Data", date.today())
    tipo = st.selectbox("Tipo", ["trail", "corrida", "caminhada", "bike"])
    distancia = st.number_input("Distância (km)")
    duracao = st.number_input("Duração (min)")
    pace = st.number_input("Pace")
    fc = st.number_input("FC média")
    dplus = st.number_input("D+")
    notas = st.text_area("Notas")

    if st.button("Guardar treino"):
        conn = get_conn()
        c = conn.cursor()

        c.execute("""
        INSERT INTO treinos
        (user_id, data, tipo, distancia, duracao, pace, fc, dplus, notas)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            str(data),
            tipo,
            distancia,
            duracao,
            pace,
            fc,
            dplus,
            notas
        ))

        conn.commit()
        st.success("Guardado")

    # HISTÓRICO
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM treinos WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    for r in rows:
        st.write(r)
