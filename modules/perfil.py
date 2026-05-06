import streamlit as st
from database import get_conn
from datetime import date
import pandas as pd


def calcular_imc(peso, altura_cm):
    altura_m = altura_cm / 100
    return peso / (altura_m ** 2)


def interpretacao_imc(imc):
    if imc < 18.5:
        return "🔵 Baixo peso"
    elif imc < 25:
        return "🟢 Normal"
    elif imc < 30:
        return "🟡 Sobrepeso"
    else:
        return "🔴 Obesidade"


def render_perfil(user_id):
    st.title("Perfil")

    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT * FROM perfil WHERE user_id=?", (user_id,))
    data = c.fetchone()

    nome = st.text_input("Nome", value=data[1] if data else "")

    nascimento = st.date_input(
        "Data nascimento",
        value=date(1990, 1, 1),
        min_value=date(1920, 1, 1),
        max_value=date.today(),
        key="birth"
    )

    altura = st.number_input("Altura (cm)", value=data[3] if data else 170)

    if st.button("Guardar Perfil", use_container_width=True):
        c.execute("""
        INSERT OR REPLACE INTO perfil (user_id, nome, data_nascimento, altura)
        VALUES (?, ?, ?, ?)
        """, (user_id, nome, str(nascimento), altura))
        conn.commit()
        st.success("Guardado")

    # PESO
    st.divider()
    peso = st.number_input("Peso atual (kg)")

    if peso > 0 and altura > 0:
        imc = calcular_imc(peso, altura)
        estado = interpretacao_imc(imc)

        st.metric("IMC", round(imc, 1))
        st.progress(min(imc / 40, 1.0))
        st.info(estado)

        # Idade metabólica (simples)
        idade_real = date.today().year - nascimento.year
        idade_met = int(idade_real + (imc - 22))

        st.metric("Idade metabólica", idade_met)
        st.progress(min(idade_met / 80, 1.0))

    if st.button("Registar Peso"):
        c.execute("""
        INSERT INTO peso (user_id, data, peso)
        VALUES (?, ?, ?)
        """, (user_id, str(date.today()), peso))
        conn.commit()

    c.execute("SELECT data, peso FROM peso WHERE user_id=?", (user_id,))
    rows = c.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=["Data", "Peso"])
        df["Data"] = pd.to_datetime(df["Data"])
        st.line_chart(df.set_index("Data"))
