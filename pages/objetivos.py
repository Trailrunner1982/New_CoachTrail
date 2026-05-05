import streamlit as st
from database import get_conn

def objetivos_page(user_id):
    st.header("Objetivo")

    nome = st.text_input("Nome prova")
    data = st.date_input("Data")
    dist = st.number_input("Distância (km)")
    dplus = st.number_input("D+")
    prioridade = st.selectbox("Prioridade", ["A", "B", "C"])

    if st.button("Guardar objetivo"):
        conn = get_conn()
        c = conn.cursor()

        c.execute("""
        INSERT INTO objetivos (user_id, nome, data, distancia, dplus, prioridade)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, nome, str(data), dist, dplus, prioridade))

        conn.commit()
        st.success("Guardado")
