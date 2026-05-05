import streamlit as st
from database import get_conn
from treino_engine import gerar_plano
from datetime import date


def render_plano(user_id):
    st.header("Plano")

    conn = get_conn()
    c = conn.cursor()

    # OBJETIVO A
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

    if st.button("Gerar Plano"):
        plano = gerar_plano(data_inicio, data_fim)

        for t in plano:
            c.execute("""
            INSERT INTO plano (user_id, data, tipo, descricao, status)
            VALUES (?, ?, ?, ?, ?)
            """, (user_id, t["data"], t["tipo"], t["descricao"], "planeado"))

        conn.commit()
        st.success("Plano gerado")

    # MOSTRAR
    c.execute("SELECT * FROM plano WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    for r in rows:
        st.write(f"{r[2]} - {r[3]}")

        col1, col2, col3 = st.columns(3)
        if col1.button("Feito", key=f"f{r[0]}"):
            c.execute("UPDATE plano SET status='feito' WHERE id=?", (r[0],))
            conn.commit()
        if col2.button("Falhou", key=f"x{r[0]}"):
            c.execute("UPDATE plano SET status='falhou' WHERE id=?", (r[0],))
            conn.commit()
        if col3.button("Doente", key=f"d{r[0]}"):
            c.execute("UPDATE plano SET status='doente' WHERE id=?", (r[0],))
            conn.commit()
