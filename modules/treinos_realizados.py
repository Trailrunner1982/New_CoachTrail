import streamlit as st
from database import get_conn
from datetime import date


def render_treinos(user_id):
    st.title("Treinos Realizados")

    conn = get_conn()
    c = conn.cursor()

    data = st.date_input("Data", date.today())
    tipo = st.selectbox("Tipo", ["Trail", "Corrida", "Bike"])
    dist = st.number_input("Distância (km)")
    dur = st.number_input("Duração (min)")

    if st.button("Guardar"):
        c.execute("""
        INSERT INTO treinos (user_id, data, tipo, distancia, duracao)
        VALUES (?, ?, ?, ?, ?)
        """, (user_id, str(data), tipo, dist, dur))
        conn.commit()

    st.divider()

    c.execute("""
    SELECT data, tipo, distancia, duracao
    FROM treinos WHERE user_id=?
    ORDER BY data DESC
    """, (user_id,))
    rows = c.fetchall()

    for r in rows:
        with st.container():
            st.markdown(f"""
### 🏃 {r[1]}  
📅 {r[0]}  
📏 {r[2]} km | ⏱ {r[3]} min
""")
            st.divider()
