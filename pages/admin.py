import streamlit as st
from database import get_conn

def admin_page():

    st.header("Admin")

    username = st.text_input("Username")
    password = st.text_input("Password")

    if st.button("Criar atleta"):
        conn = get_conn()
        c = conn.cursor()

        c.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, 'athlete')
        """, (username, password))

        conn.commit()
        st.success("Criado")

    st.subheader("Atletas")

    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT id, username FROM users WHERE role='athlete'")
    atletas = c.fetchall()

    for a in atletas:
        if st.button(a[1]):
            st.session_state["user_id"] = a[0]
            st.rerun()
