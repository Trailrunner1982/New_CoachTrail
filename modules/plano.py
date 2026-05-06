import streamlit as st
from database import get_conn
import pandas as pd


def cor(tipo):
    if "Intervalado" in tipo:
        return "red"
    elif "Endurance" in tipo:
        return "blue"
    elif "Descanso" in tipo:
        return "gray"
    else:
        return "green"


def render_plano(user_id):
    st.title("Plano de Treino")

    conn = get_conn()
    c = conn.cursor()

    c.execute("""
    SELECT id, data, tipo, descricao, status
    FROM plano
    WHERE user_id=?
    ORDER BY data
    """, (user_id,))
    rows = c.fetchall()

    if not rows:
        st.warning("Ainda não tens plano gerado")
        return

    df = pd.DataFrame(rows, columns=["id","data","tipo","descricao","status"])
    df["data"] = pd.to_datetime(df["data"])
    df["week"] = df["data"].dt.isocalendar().week

    semanas = df["week"].unique()

    for semana in semanas:

        st.subheader(f"Semana {semana}")

        semana_df = df[df["week"] == semana]

        cols = st.columns(7)

        for i, (_, row) in enumerate(semana_df.iterrows()):
            with cols[i % 7]:

                cor_css = cor(row["tipo"])

                st.markdown(f"""
                <div class="card {cor_css}">
                <b>{row['data'].day}</b><br>
                {row['tipo']}<br>
                {row['status']}
                </div>
                """, unsafe_allow_html=True)

                if st.button("Ver", key=f"ver{row['id']}"):
                    st.session_state["treino_sel"] = row["id"]

    # =========================
    # DETALHE TREINO
    # =========================
    if "treino_sel" in st.session_state:
        treino_id = st.session_state["treino_sel"]

        c.execute("""
        SELECT data, descricao FROM plano
        WHERE id=?
        """, (treino_id,))
        t = c.fetchone()

        st.divider()
        st.subheader(f"Treino {t[0]}")
        st.write(t[1])
