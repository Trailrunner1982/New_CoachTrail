import streamlit as st
from database import get_conn
from treino_engine import gerar_plano
from datetime import date
import pandas as pd


def cor_status(status):
    if status == "feito":
        return "🟢"
    elif status == "falhou":
        return "🔴"
    elif status == "doente":
        return "⚫"
    else:
        return "🔵"


def render_plano(user_id):
    st.title("Plano de Treino")

    conn = get_conn()
    c = conn.cursor()

    # =========================
    # OBJETIVO A
    # =========================
    c.execute("""
    SELECT * FROM objetivos
    WHERE user_id=? AND prioridade='A'
    ORDER BY data LIMIT 1
    """, (user_id,))
    obj = c.fetchone()

    if not obj:
        st.warning("Define um objetivo prioridade A")
        return

    data_fim = date.fromisoformat(obj[3])
    data_inicio = date.today()

    # =========================
    # GERAR PLANO
    # =========================
    if st.button("Gerar Plano", use_container_width=True):

        c.execute("DELETE FROM plano WHERE user_id=?", (user_id,))
        conn.commit()

        plano = gerar_plano(data_inicio, data_fim)

        for t in plano:
            c.execute("""
            INSERT INTO plano (user_id, data, tipo, descricao, status)
            VALUES (?, ?, ?, ?, ?)
            """, (user_id, t["data"], t["tipo"], t["descricao"], "planeado"))

        conn.commit()
        st.success("Plano gerado")
        st.rerun()

    # =========================
    # BUSCAR PLANO
    # =========================
    c.execute("""
    SELECT id, data, tipo, descricao, status
    FROM plano
    WHERE user_id=?
    ORDER BY data
    """, (user_id,))
    rows = c.fetchall()

    if not rows:
        st.info("Ainda não existe plano")
        return

    df = pd.DataFrame(rows, columns=["id", "data", "tipo", "descricao", "status"])
    df["data"] = pd.to_datetime(df["data"])

    # =========================
    # AGRUPAR POR SEMANA
    # =========================
    df["week"] = df["data"].dt.isocalendar().week

    semanas = df["week"].unique()

    for semana in semanas:

        st.subheader(f"Semana {semana}")

        semana_df = df[df["week"] == semana]

        for _, row in semana_df.iterrows():

            with st.expander(f"{cor_status(row['status'])} {row['data'].date()} - {row['tipo']}"):

                st.write(row["descricao"])

                col1, col2, col3 = st.columns(3)

                if col1.button("Feito", key=f"f{row['id']}"):
                    c.execute("UPDATE plano SET status='feito' WHERE id=?", (row["id"],))
                    conn.commit()
                    st.rerun()

                if col2.button("Falhou", key=f"x{row['id']}"):
                    c.execute("UPDATE plano SET status='falhou' WHERE id=?", (row["id"],))
                    conn.commit()
                    st.rerun()

                if col3.button("Doente", key=f"d{row['id']}"):
                    c.execute("UPDATE plano SET status='doente' WHERE id=?", (row["id"],))
                    conn.commit()
                    st.rerun()

        st.divider()
