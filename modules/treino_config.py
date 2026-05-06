import streamlit as st
from database import get_conn


def render_treino(user_id):
    st.title("Configuração de Treino")

    conn = get_conn()
    c = conn.cursor()

    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    dias = st.multiselect(
        "Dias disponíveis",
        dias_semana,
        help="Seleciona os dias em que podes treinar"
    )

    dia_longo = st.selectbox("Dia do treino longo", dias if dias else dias_semana)

    volume = st.number_input(
        "Volume semanal (km)",
        help="Quantos km costumas fazer por semana"
    )

    pace = st.number_input(
        "Pace médio (min/km)",
        help="Exemplo: 5.30 = 5min30/km"
    )

    st.subheader("Treino de Força")

    forca = st.checkbox("Incluir treino de força")

    forca_dias = []
    if forca:
        forca_dias = st.multiselect(
            "Dias de força",
            dias_semana,
            help="Podes escolher dias diferentes dos treinos"
        )

    if st.button("Guardar", use_container_width=True):
        c.execute("""
        INSERT OR REPLACE INTO treino_config
        (user_id, dias, dia_longo, volume_km, pace, forca, forca_dias)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            ",".join(dias),
            dia_longo,
            volume,
            pace,
            int(forca),
            ",".join(forca_dias)
        ))
        conn.commit()
        st.success("Guardado")
