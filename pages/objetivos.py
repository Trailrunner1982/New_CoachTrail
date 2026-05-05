import streamlit as st
from database import get_conn


def objetivos_page(user_id):
    st.header("Objetivos")

    nome = st.text_input("Nome do objetivo/prova")
    data = st.date_input("Data")

    distancia = st.number_input("Distância (km)")
    dplus = st.number_input("D+")

    tempo = st.text_input("Tempo objetivo (opcional)")

    prioridade = st.selectbox("Prioridade", ["A", "B", "C"])

    if st.button("Guardar objetivo"):
        conn = get_conn()
        c = conn.cursor()

        c.execute("""
        INSERT INTO objetivos
        (user_id, nome, data, distancia, dplus, tempo_objetivo, prioridade)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            nome,
            str(data),
            distancia,
            dplus,
            tempo,
            prioridade
        ))

        conn.commit()
        st.success("Guardado")
