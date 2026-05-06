import streamlit as st
from database import get_conn
from engine import readiness_score, gerar_treino
from datetime import date


def render_dashboard(user_id):

    st.title("Dashboard")

    hrv = st.slider("HRV", 1, 10, 5)
    sleep = st.slider("Sono", 1, 10, 7)
    body = st.slider("Body Battery", 1, 100, 50)
    rhr = st.slider("FC repouso", 40, 80, 60)
    stress = st.slider("Stress", 1, 10, 5)

    if st.button("Check-in"):

        score, status = readiness_score(hrv, sleep, body, rhr, stress)

        treino = gerar_treino(status)

        st.metric("Readiness", score)
        st.write(status)
        st.success(treino)
