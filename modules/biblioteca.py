import streamlit as st
from database import get_conn


def render_biblioteca():
    st.title("Biblioteca")

    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM biblioteca")
    rows = c.fetchall()

    for r in rows:
        st.subheader(r[1])
        st.write(r[2])
