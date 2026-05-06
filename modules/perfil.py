import streamlit as st
from database import get_conn
from datetime import date
import pandas as pd


def render_perfil(user_id):
    st.title("Perfil")

    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM perfil WHERE user_id=?", (user_id,))
    data = c.fetchone()

    nome = st.text_input("Nome", value=data[1] if data else "")

    nascimento = st.date_input(
        "Data nascimento",
        value=date(1990, 1, 1),
        min_value=date(1920, 1, 1),
        max_value=date.today()
    )

    altura = st.number_input("Altura (cm)", value=data[3] if data else 170)

    if st.button("Guardar Perfil", use_container_width=True):
        c.execute("""
        INSERT OR REPLACE INTO perfil (user_id, nome, data_nascimento, altura)
        VALUES (?, ?, ?, ?)
        """, (user_id, nome, str(nascimento), altura))
        conn.commit()
        st.success("Guardado")
