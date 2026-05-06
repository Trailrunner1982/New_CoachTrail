import streamlit as st
from database import get_conn


def login():

    st.title("UltraCoach Login")

    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Entrar"):

        conn = get_conn()
        c = conn.cursor()

        c.execute("SELECT id, role FROM users WHERE username=? AND password=?", (user, pwd))
        res = c.fetchone()

        if res:
            st.session_state["user_id"] = res[0]
            st.session_state["role"] = res[1]
            st.session_state["logged"] = True
            st.rerun()
        else:
            st.error("Credenciais inválidas")
