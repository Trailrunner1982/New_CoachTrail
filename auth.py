import streamlit as st
from database import get_conn

def login():
    st.title("Login")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Entrar"):
        conn = get_conn()
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pw))
        res = c.fetchone()

        if res:
            st.session_state["user_id"] = res[0]
            st.session_state["role"] = res[3]
            st.success("Login OK")
            st.rerun()
        else:
            st.error("Credenciais inválidas")
