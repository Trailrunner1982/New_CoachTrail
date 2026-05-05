import streamlit as st
from database import get_conn
from treino_engine import gerar_plano

def plano_page(user_id):

    st.header("Plano de Treino")

    conn = get_conn()
    c = conn.cursor()

    # user
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    u = c.fetchone()

    user = {
        "id": u[0],
        "fc_max": u[5],
        "fc_repouso": u[6],
        "dias_treino": list(map(int, u[7].split(","))),
        "dia_longo": u[8],
        "volume_atual_horas": u[9],
        "nivel": "intermedio"
    }

    # objetivo A
    c.execute("""
    SELECT * FROM objetivos
    WHERE user_id=? AND prioridade='A'
    ORDER BY data LIMIT 1
    """, (user_id,))
    obj = c.fetchone()

    if not obj:
        st.warning("Sem objetivo A")
        return

    objetivo = {
        "data": obj[3],
        "distancia": obj[4],
        "dplus": obj[5]
    }

    if st.button("Gerar plano"):
        plano = gerar_plano(user, objetivo, historico=[])

        # guardar
        for semana in plano:
            for t in semana["treinos"]:
                c.execute("""
                INSERT INTO plano (user_id, data, tipo, duracao, descricao, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    str(t["dia"]),
                    t["tipo"],
                    t["duracao_horas"],
                    str(t["zonas"]),
                    "planeado"
                ))

        conn.commit()
        st.success("Plano gerado")

    # mostrar plano
    c.execute("SELECT * FROM plano WHERE user_id=?", (user_id,))
    dados = c.fetchall()

    for d in dados:
        st.write(d)
