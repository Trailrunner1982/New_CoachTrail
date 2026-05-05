import streamlit as st
from database import get_conn
from treino_engine import gerar_plano
from services.recomendador import obter_recomendacoes


def plano_page(user_id):

    st.header("Plano de Treino")

    conn = get_conn()
    c = conn.cursor()

    # USER
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    u = c.fetchone()

    user = {
        "id": u[0],
        "fc_max": u[5],
        "fc_repouso": u[6],
        "dias_treino": list(map(int, u[7].split(","))) if u[7] else [],
        "dia_longo": u[8],
        "volume_atual_horas": u[9] or 3,
        "nivel": "intermedio"
    }

    # OBJETIVO
    c.execute("""
    SELECT * FROM objetivos
    WHERE user_id=? AND prioridade='A'
    ORDER BY data LIMIT 1
    """, (user_id,))
    obj = c.fetchone()

    if not obj:
        st.warning("Define um objetivo primeiro")
        return

    objetivo = {
        "data": obj[3],
        "distancia": obj[4],
        "dplus": obj[5]
    }

    # GERAR PLANO
    if st.button("Gerar plano"):
        plano = gerar_plano(user, objetivo, historico=[])

        for semana in plano["plano"]:
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

    # MOSTRAR
    c.execute("SELECT * FROM plano WHERE user_id=?", (user_id,))
    dados = c.fetchall()

    for d in dados:
        st.subheader(f"Treino: {d[3]}")
        st.write(f"Duração: {d[4]}h")
        st.write(f"Zonas: {d[5]}")

        # 🔥 RECOMENDAÇÕES
        treino_fake = {
            "tipo": d[3],
            "forca": "forca" in d[5]
        }

        recs = obter_recomendacoes(treino_fake)

        if recs:
            st.write("💡 Recomendações:")
            for r in recs:
                st.write(f"- {r['titulo']}")
                if "link" in r:
                    st.video(r["link"])

        st.write("---")
