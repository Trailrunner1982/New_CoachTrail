import streamlit as st
from database import get_conn


def render_treino(user_id):
    st.title("Configuração de Treino")

    conn = get_conn()
    c = conn.cursor()

    dias = st.multiselect(
        "Dias disponíveis",
        ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    )

    dia_longo = st.selectbox(
        "Dia do treino longo",
        dias if dias else ["Sáb"]
    )

    volume = st.number_input("Volume semanal (km)", help="Se não souber, deixa 0")
    pace = st.number_input("Pace médio (min/km)", help="Ex: 5.30")

    st.subheader("Treino de Força")
    forca = st.checkbox("Incluir treino de força")

    forca_dias = []
    if forca:
        forca_dias = st.multiselect("Dias de força", dias)

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
