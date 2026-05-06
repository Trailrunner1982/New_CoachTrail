import streamlit as st
from database import get_conn


def render_admin():

    st.title("Admin")

    conn = get_conn()
    c = conn.cursor()

    st.subheader("Criar Atleta")

    user = st.text_input("Username")
    pwd = st.text_input("Password")

    if st.button("Criar"):

        c.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, 'athlete')
        """, (user, pwd))

        conn.commit()
        st.success("Criado")

    st.divider()

    c.execute("SELECT id, username FROM users WHERE role='athlete'")
    atletas = c.fetchall()

    for a in atletas:
        st.write(a)
