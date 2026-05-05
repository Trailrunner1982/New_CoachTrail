import streamlit as st
from database import get_conn


def perfil_page(user_id):
    st.header("Perfil Pessoal")

    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM perfil WHERE user_id=?", (user_id,))
    p = c.fetchone()

    nome = st.text_input("Nome", value=p[1] if p else "")
    data = st.date_input("Data de nascimento")
    altura = st.number_input("Altura (cm)", value=p[3] if p else 170)
    peso = st.number_input("Peso (kg)", value=p[4] if p else 70)

    if st.button("Guardar perfil"):
        c.execute("""
        INSERT OR REPLACE INTO perfil (user_id, nome, data_nascimento, altura, peso)
        VALUES (?, ?, ?, ?, ?)
        """, (user_id, nome, str(data), altura, peso))
        conn.commit()
        st.success("Perfil guardado")
