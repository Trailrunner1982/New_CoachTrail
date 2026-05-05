import streamlit as st
from database import get_conn


def biblioteca_page():
    st.header("Biblioteca")

    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM biblioteca")
    items = c.fetchall()

    for i in items:
        st.subheader(i[1])
        st.write(f"Tipo: {i[2]}")
        st.write(i[4])

        if i[2] == "video":
            st.video(i[3])
        else:
            st.markdown(f"[Abrir artigo]({i[3]})")

        st.write("---")
