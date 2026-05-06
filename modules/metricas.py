import streamlit as st
from database import get_conn
from datetime import date
import pandas as pd


def render_metricas(user_id):
    st.title("Métricas Diárias")

    conn = get_conn()
    c = conn.cursor()

    hrv = st.number_input("HRV", help="Variabilidade cardíaca")
    rhr = st.number_input("FC repouso")
    sleep = st.number_input("Sleep Score")
    body = st.number_input("Body Battery")
    vo2 = st.number_input("VO2 Max")

    if st.button("Guardar", use_container_width=True):
        c.execute("""
        INSERT INTO metricas
        (user_id, data, hrv, rhr, sleep, body, vo2)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            str(date.today()),
            hrv,
            rhr,
            sleep,
            body,
            vo2
        ))
        conn.commit()
        st.success("Guardado")

    st.divider()

    c.execute("SELECT data, hrv, rhr, sleep, body, vo2 FROM metricas WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=["Data", "HRV", "RHR", "Sleep", "Body", "VO2"])
        df["Data"] = pd.to_datetime(df["Data"])

        st.dataframe(df, use_container_width=True)
        st.line_chart(df.set_index("Data")[["HRV"]])
