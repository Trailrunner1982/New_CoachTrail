import streamlit as st
from database import get_conn
import pandas as pd
from datetime import date


def render_treinos(user_id):
    st.title("Treinos Realizados")

    conn = get_conn()
    c = conn.cursor()

    data = st.date_input("Data", date.today())
    tipo = st.selectbox("Tipo", ["trail", "corrida", "bike", "caminhada"])
    dist = st.number_input("Distância (km)")
    dur = st.number_input("Duração (min)")
    fc = st.number_input("FC média")

    if st.button("Guardar", use_container_width=True):
        c.execute("""
        INSERT INTO treinos (user_id, data, tipo, distancia, duracao, fc)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, str(data), tipo, dist, dur, fc))
        conn.commit()
        st.success("Guardado")

    # 🔥 TABELA
    c.execute("""
    SELECT data, tipo, distancia, duracao, fc
    FROM treinos WHERE user_id=?
    ORDER BY data DESC
    """, (user_id,))
    rows = c.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=["Data", "Tipo", "Distância", "Duração", "FC"])
        st.dataframe(df, use_container_width=True)
