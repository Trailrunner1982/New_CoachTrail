import streamlit as st
from database import get_conn
from datetime import date
import pandas as pd


def render_treinos(user_id):

    st.title("Treinos Realizados")

    conn = get_conn()
    c = conn.cursor()

    data = st.date_input("Data", value=date.today())
    tipo = st.selectbox("Tipo", ["Trail", "Corrida", "Bicicleta", "Caminhada"])

    distancia = st.number_input("Distância (km)")
    duracao = st.text_input("Duração (HH:MM:SS)")
    pace = st.number_input("Pace (min/km)")
    alt = st.number_input("Altimetria (D+)")

    fc_media = st.number_input("FC Média")
    fc_max = st.number_input("FC Máxima")

    rpe = st.slider("RPE (1-10)", 1, 10, 5)

    notas = st.text_area("Notas")

    if st.button("Guardar Treino"):

        c.execute("""
        INSERT INTO treinos
        (user_id,data,tipo,distancia,duracao,pace,altimetria,fc_media,fc_max,rpe,notas)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            user_id,
            data.isoformat(),
            tipo,
            distancia,
            duracao,
            pace,
            alt,
            fc_media,
            fc_max,
            rpe,
            notas
        ))

        conn.commit()
        st.success("Treino guardado")

    st.divider()

    c.execute("SELECT * FROM treinos WHERE user_id=? ORDER BY data DESC", (user_id,))
    rows = c.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=[
            "id","user","data","tipo","dist","dur","pace","d+","fc_med","fc_max","rpe","notas"
        ])
        st.dataframe(df, use_container_width=True)
