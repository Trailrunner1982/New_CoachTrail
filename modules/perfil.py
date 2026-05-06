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

    st.subheader("Dados Pessoais")

    nome = st.text_input("Nome", value=data[1] if data else "")

    nascimento = st.date_input(
        "Data nascimento",
        max_value=date.today(),
        help="Seleciona a tua data real de nascimento"
    )

    altura = st.number_input("Altura (cm)", value=data[3] if data else 170)

    if st.button("Guardar Perfil", use_container_width=True):
        c.execute("""
        INSERT OR REPLACE INTO perfil (user_id, nome, data_nascimento, altura)
        VALUES (?, ?, ?, ?)
        """, (user_id, nome, str(nascimento), altura))
        conn.commit()
        st.success("Guardado")

    # PESO
    st.divider()
    st.subheader("Peso")

    peso = st.number_input("Peso atual (kg)", help="Regista regularmente para acompanhar evolução")

    if st.button("Registar Peso", use_container_width=True):
        c.execute("""
        INSERT INTO peso (user_id, data, peso)
        VALUES (?, ?, ?)
        """, (user_id, str(date.today()), peso))
        conn.commit()
        st.success("Registado")

    c.execute("SELECT data, peso FROM peso WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=["Data", "Peso"])
        df["Data"] = pd.to_datetime(df["Data"])

        st.line_chart(df.set_index("Data"))
        st.dataframe(df)
