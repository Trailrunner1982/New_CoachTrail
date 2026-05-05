import streamlit as st
from database import get_conn


def treino_page(user_id):
    st.header("Configuração de Treino")

    conn = get_conn()
    c = conn.cursor()

    dias = st.multiselect(
        "Dias de treino",
        ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
    )

    dia_longo = st.selectbox(
        "Dia do treino longo",
        ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
    )

    volume_km = st.number_input("Volume semanal (km)", value=0.0)
    volume_horas = st.number_input("Volume semanal (horas)", value=3.0)

    preferencia = st.selectbox(
        "Tipo principal",
        ["trail", "corrida", "ciclismo"]
    )

    if st.button("Guardar configuração"):
        c.execute("""
        INSERT OR REPLACE INTO treino_config
        (user_id, dias_treino, dia_longo, volume_km, volume_horas, preferencia)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            ",".join(dias),
            dia_longo,
            volume_km,
            volume_horas,
            preferencia
        ))
        conn.commit()
        st.success("Guardado")
