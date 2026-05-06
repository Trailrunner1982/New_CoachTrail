import streamlit as st
from database import get_conn
from datetime import date
import pandas as pd


def interpretar(hrv, rhr):
    if hrv > 60 and rhr < 55:
        return "🟢 Excelente recuperação"
    elif hrv > 45:
        return "🟡 Estado moderado"
    else:
        return "🔴 Fadiga elevada"


def render_metricas(user_id):
    st.title("Métricas")

    conn = get_conn()
    c = conn.cursor()

    hrv = st.number_input("HRV")
    rhr = st.number_input("FC repouso")
    sleep = st.number_input("Sleep Score")
    body = st.number_input("Body Battery")
    vo2 = st.number_input("VO2 Max")

    estado = interpretar(hrv, rhr)
    st.info(f"Estado: {estado}")

    if st.button("Guardar", use_container_width=True):
        c.execute("""
        INSERT INTO metricas
        (user_id, data, hrv, rhr, sleep, body, vo2)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, str(date.today()), hrv, rhr, sleep, body, vo2))
        conn.commit()
        st.success("Guardado")

    c.execute("SELECT data, hrv, rhr FROM metricas WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=["Data", "HRV", "RHR"])
        df["Data"] = pd.to_datetime(df["Data"])
        st.line_chart(df.set_index("Data"))
