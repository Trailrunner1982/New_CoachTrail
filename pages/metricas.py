import streamlit as st
from database import get_conn
from datetime import date


def metricas_page(user_id):
    st.header("Métricas Diárias")

    conn = get_conn()
    c = conn.cursor()

    hrv = st.number_input("HRV")
    rhr = st.number_input("RHR")
    sleep = st.number_input("Sleep Score")
    body = st.number_input("Body Battery")
    vo2 = st.number_input("VO2 Max")

    if st.button("Guardar métricas"):
        c.execute("""
        INSERT INTO metricas
        (user_id, data, hrv, rhr, sleep, body_battery, vo2)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, str(date.today()), hrv, rhr, sleep, body, vo2))
        conn.commit()
        st.success("Guardado")

    # Histórico
    c.execute("SELECT * FROM metricas WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    for r in rows:
        st.write(r)
