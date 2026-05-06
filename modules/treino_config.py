import streamlit as st
from database import get_conn


def render_treino(user_id):
    st.title("Configuração de Treino")

    conn = get_conn()
    c = conn.cursor()

    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    dias = st.multiselect("Dias de treino", dias_semana)

    dia_longo = st.selectbox("Dia longo", dias_semana)

    volume = st.number_input("Volume semanal (km)")
    pace = st.number_input("Pace médio")

    forca = st.checkbox("Treino de força")

    forca_dias = []
    if forca:
        forca_dias = st.multiselect("Dias força", dias_semana)

    # 🔥 RESUMO VISUAL
    st.info(f"""
📌 Resumo:
Dias: {dias}
Longo: {dia_longo}
Volume: {volume} km
Pace: {pace}
Força: {forca_dias}
""")

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
