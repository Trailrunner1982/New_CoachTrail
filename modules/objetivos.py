import streamlit as st
from database import get_conn
import pandas as pd


def render_objetivos(user_id):
    st.title("Objetivos")

    conn = get_conn()
    c = conn.cursor()

    tipo = st.radio("Tipo de objetivo", ["Prova", "Objetivo Livre"])

    if tipo == "Prova":

        nome = st.text_input("Nome da prova")
        data = st.date_input("Data")
        dist = st.number_input("Distância (km)")
        dplus = st.number_input("D+")

        modo = st.radio("Objetivo", ["Finalizar", "Tempo alvo"])

        tempo = None
        if modo == "Tempo alvo":
            tempo = st.text_input("Tempo (HH:MM)")

        prioridade = st.selectbox("Prioridade", ["A", "B", "C"])

        if st.button("Adicionar Prova", use_container_width=True):
            c.execute("""
            INSERT INTO objetivos
            (user_id, nome, data, distancia, dplus, tempo, prioridade)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, nome, str(data), dist, dplus, tempo, prioridade))
            conn.commit()
            st.success("Adicionado")

    else:
        dist = st.number_input("Distância (km)")
        tempo = st.text_input("Tempo alvo (HH:MM)")
        data = st.date_input("Data")

        if st.button("Adicionar Objetivo", use_container_width=True):
            c.execute("""
            INSERT INTO objetivos
            (user_id, nome, data, distancia, tempo, prioridade)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, "Objetivo Livre", str(data), dist, tempo, "A"))
            conn.commit()
            st.success("Adicionado")

    st.divider()

    st.subheader("Tabela de Objetivos")

    c.execute("SELECT nome, data, distancia, dplus, tempo, prioridade FROM objetivos WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=["Nome", "Data", "Distância", "D+", "Tempo", "Prioridade"])
        st.dataframe(df, use_container_width=True)
