import streamlit as st
from database import get_conn
from datetime import date
import pandas as pd


def render_objetivos(user_id):

    st.title("Objetivos & Provas")

    conn = get_conn()
    c = conn.cursor()

    # =========================
    # TIPO DE OBJETIVO
    # =========================
    tipo = st.radio("Tipo", ["Prova", "Objetivo Pessoal"])

    nome = st.text_input("Nome")

    data_obj = st.date_input("Data", value=date.today())

    prioridade = st.selectbox("Prioridade", ["A", "B", "C"])

    distancia = st.number_input("Distância (km)", step=0.1)

    altimetria = st.number_input("Altimetria D+")

    # =========================
    # ESPECÍFICO PROVA
    # =========================
    tempo_obj = None
    terminar = False

    if tipo == "Prova":

        terminar = st.checkbox("Apenas finalizar")

        if not terminar:
            tempo_obj = st.text_input("Tempo alvo (HH:MM:SS)")

    # =========================
    # GUARDAR
    # =========================
    if st.button("Guardar Objetivo"):

        if not nome:
            st.error("Nome obrigatório")
            return

        c.execute("""
        INSERT INTO objetivos
        (user_id, nome, data, distancia, altimetria, prioridade)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            nome,
            data_obj.isoformat(),
            distancia,
            altimetria,
            prioridade
        ))

        conn.commit()
        st.success("Guardado")

    st.divider()

    # =========================
    # LISTAGEM
    # =========================
    st.subheader("Objetivos definidos")

    c.execute("""
    SELECT id, nome, data, distancia, altimetria, prioridade
    FROM objetivos
    WHERE user_id=?
    ORDER BY data
    """, (user_id,))

    rows = c.fetchall()

    if rows:

        df = pd.DataFrame(rows, columns=[
            "ID","Nome","Data","Distância","D+","Prioridade"
        ])

        st.dataframe(df, use_container_width=True)

        # =========================
        # DELETE
        # =========================
        ids = df["ID"].tolist()

        del_id = st.selectbox("Remover objetivo", ids)

        if st.button("Eliminar"):
            c.execute("DELETE FROM objetivos WHERE id=?", (del_id,))
            conn.commit()
            st.success("Removido")
            st.rerun()

    else:
        st.info("Sem objetivos ainda")
