import streamlit as st
from database import get_conn
from datetime import date


def render_perfil(user_id):

    st.title("Perfil do Atleta")

    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM perfil WHERE user_id=?", (user_id,))
    p = c.fetchone()

    nome = st.text_input("Nome", value=p[1] if p else "")

    nascimento = st.date_input(
        "Data de nascimento",
        value=date(1990,1,1) if not p else date.fromisoformat(p[2])
    )

    altura = st.number_input("Altura (cm)", value=p[3] if p else 170.0)
    peso = st.number_input("Peso atual", value=p[4] if p else 70.0)

    fc_max = st.number_input("FC Máx", value=p[5] if p else 180)
    fc_rep = st.number_input("FC Repouso", value=p[6] if p else 60)

    if st.button("Guardar Perfil"):

        c.execute("""
        INSERT OR REPLACE INTO perfil
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            nome,
            nascimento.isoformat(),
            altura,
            peso,
            fc_max,
            fc_rep
        ))

        c.execute("""
        INSERT INTO peso_log (user_id, data, peso)
        VALUES (?, ?, ?)
        """, (user_id, date.today().isoformat(), peso))

        conn.commit()
        st.success("Guardado")
