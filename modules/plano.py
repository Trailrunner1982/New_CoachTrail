import streamlit as st
from database import get_conn
from treino_engine import gerar_plano_prova
from datetime import date
import pandas as pd


def render_plano(user_id):

    st.title("Plano de Treino (Periodizado)")

    conn = get_conn()
    c = conn.cursor()

    # buscar prova A
    c.execute("""
    SELECT data FROM objetivos
    WHERE user_id=? AND prioridade='A'
    ORDER BY data LIMIT 1
    """, (user_id,))
    obj = c.fetchone()

    if not obj:
        st.warning("Define uma prova prioridade A")
        return

    data_prova = date.fromisoformat(obj[0])

    if st.button("Gerar Plano Completo"):

        c.execute("DELETE FROM plano WHERE user_id=?", (user_id,))
        conn.commit()

        plano = gerar_plano_prova(date.today(), data_prova)

        for t in plano:
            c.execute("""
            INSERT INTO plano (user_id, data, tipo, descricao, status)
            VALUES (?, ?, ?, ?, 'planeado')
            """, (user_id, t["data"], t["tipo"], t["descricao"]))

        conn.commit()
        st.success("Plano estruturado criado")
        st.rerun()

    # LOAD
    c.execute("SELECT id, data, tipo, descricao, status FROM plano WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    if not rows:
        st.info("Sem plano ainda")
        return

    df = pd.DataFrame(rows, columns=["id","data","tipo","descricao","status"])
    df["data"] = pd.to_datetime(df["data"])
    df["week"] = df["data"].dt.isocalendar().week

    for semana in df["week"].unique():

        st.subheader(f"Semana {semana}")

        semana_df = df[df["week"] == semana]

        cols = st.columns(7)

        for i, (_, row) in enumerate(semana_df.iterrows()):

            with cols[i % 7]:

                st.markdown(f"""
                <div style="
                padding:10px;
                border-radius:10px;
                background:#2b5da8;
                color:white;">
                <b>{row['data'].day}</b><br>
                {row['tipo']}
                </div>
                """, unsafe_allow_html=True)

                if st.button("👁", key=f"{row['id']}"):
                    st.session_state["treino"] = row["id"]

    if "treino" in st.session_state:

        tid = st.session_state["treino"]

        c.execute("SELECT descricao FROM plano WHERE id=?", (tid,))
        desc = c.fetchone()[0]

        st.divider()
        st.subheader("Detalhe")
        st.write(desc)
