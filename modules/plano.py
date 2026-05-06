import streamlit as st
from database import get_conn
from treino_engine import gerar_plano
from datetime import date
import pandas as pd


def render_plano(user_id):

    st.title("Plano de Treino")

    conn = get_conn()
    c = conn.cursor()

    if st.button("Gerar Plano Adaptativo"):

        c.execute("DELETE FROM plano WHERE user_id=?", (user_id,))
        conn.commit()

        plano = gerar_plano(conn, user_id, date.today(), date.today().replace(month=12))

        for t in plano:
            c.execute("""
            INSERT INTO plano (user_id, data, tipo, descricao, status)
            VALUES (?, ?, ?, ?, 'planeado')
            """, (user_id, t["data"], t["tipo"], t["descricao"]))

        conn.commit()
        st.success("Plano adaptativo criado")
        st.rerun()

    # VISUAL (mantém calendário anterior)
    c.execute("SELECT id, data, tipo, descricao, status FROM plano WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    if not rows:
        st.warning("Sem plano")
        return

    df = pd.DataFrame(rows, columns=["id","data","tipo","descricao","status"])
    df["data"] = pd.to_datetime(df["data"])

    for _, row in df.iterrows():

        with st.expander(f"{row['data'].date()} - {row['tipo']}"):
            st.write(row["descricao"])

            col1, col2 = st.columns(2)

            if col1.button("Feito", key=f"f{row['id']}"):
                c.execute("UPDATE plano SET status='feito' WHERE id=?", (row["id"],))
                conn.commit()
                st.rerun()

            if col2.button("Falhou", key=f"x{row['id']}"):
                c.execute("UPDATE plano SET status='falhou' WHERE id=?", (row["id"],))
                conn.commit()
                st.rerun()
