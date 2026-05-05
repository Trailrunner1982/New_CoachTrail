import streamlit as st
from database import get_conn


def login():
    st.title("UltraCoach Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Entrar"):
        conn = get_conn()
        c = conn.cursor()

        c.execute("""
        SELECT id, role FROM users
        WHERE username=? AND password=?
        """, (username, password))

        user = c.fetchone()

        if user:
            st.session_state["user_id"] = user[0]
            st.session_state["role"] = user[1]

            # admin pode selecionar atleta depois
            st.success("Login efetuado")
            st.rerun()
        else:
            st.error("Credenciais inválidas")
