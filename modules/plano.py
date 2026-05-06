import streamlit as st
from database import get_conn
from treino_engine import gerar_plano
from datetime import date
import pandas as pd


def render_plano(user_id):

    st.title("Plano de Treino")

    conn = get_conn()
    c = conn.cursor()

    # GERAR
    if st.button("Gerar Plano Elite"):
        c.execute("DELETE FROM plano WHERE user_id=?", (user_id,))
        conn.commit()

        plano = gerar_plano(conn, user_id, date.today(), date.today().replace(month=12))

        for t in plano:
            c.execute("""
            INSERT INTO plano (user_id, data, tipo, descricao, status)
            VALUES (?, ?, ?, ?, 'planeado')
            """, (user_id, t["data"], t["tipo"], t["descricao"]))

        conn.commit()
        st.success("Plano criado")
        st.rerun()

    # LOAD
    c.execute("SELECT id, data, tipo, descricao, status FROM plano WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    if not rows:
        st.warning("Sem plano")
        return

    df = pd.DataFrame(rows, columns=["id","data","tipo","descricao","status"])
    df["data"] = pd.to_datetime(df["data"])
    df["week"] = df["data"].dt.isocalendar().week

    semanas = df["week"].unique()

    cores = {
        "Easy Run": "green",
        "Tempo Run": "yellow",
        "Intervalos": "red",
        "Long Run": "purple",
        "Descanso": "gray"
    }

    for semana in semanas:

        st.subheader(f"Semana {semana}")

        semana_df = df[df["week"] == semana]

        cols = st.columns(7)

        for i, (_, row) in enumerate(semana_df.iterrows()):

            with cols[i % 7]:

                cor = cores.get(row["tipo"], "blue")

                st.markdown(f"""
                <div style="
                padding:10px;
                border-radius:10px;
                background-color:{cor};
                color:white;
                margin-bottom:5px;">
                <b>{row['data'].day}</b><br>
                {row['tipo']}
                </div>
                """, unsafe_allow_html=True)

                if st.button("👁", key=f"v{row['id']}"):
                    st.session_state["treino"] = row["id"]

    # DETALHE
    if "treino" in st.session_state:
        tid = st.session_state["treino"]

        c.execute("SELECT descricao FROM plano WHERE id=?", (tid,))
        desc = c.fetchone()[0]

        st.divider()
        st.subheader("Detalhe do treino")
        st.write(desc)

        col1, col2, col3 = st.columns(3)

        if col1.button("✔ Feito"):
            c.execute("UPDATE plano SET status='feito' WHERE id=?", (tid,))
            conn.commit()
            st.rerun()

        if col2.button("❌ Falhou"):
            c.execute("UPDATE plano SET status='falhou' WHERE id=?", (tid,))
            conn.commit()
            st.rerun()

        if col3.button("🔁 Replanear semana"):
            c.execute("DELETE FROM plano WHERE user_id=?", (user_id,))
            conn.commit()
            st.success("Plano reset")
            st.rerun()
