import streamlit as st
from database import get_conn

def perfil_page(user_id):
    st.header("Perfil")

    fc_max = st.number_input("FC Max")
    fc_rep = st.number_input("FC Repouso")
    dias = st.multiselect("Dias treino", list(range(7)))
    longo = st.selectbox("Dia longo", list(range(7)))
    volume = st.number_input("Horas semana")

    if st.button("Guardar"):
        conn = get_conn()
        c = conn.cursor()

        c.execute("""
        UPDATE users
        SET fc_max=?, fc_repouso=?, dias_treino=?, dia_longo=?, volume_horas=?
        WHERE id=?
        """, (
            fc_max,
            fc_rep,
            ",".join(map(str, dias)),
            longo,
            volume,
            user_id
        ))

        conn.commit()
        st.success("Guardado")
