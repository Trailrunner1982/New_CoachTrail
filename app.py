import streamlit as st

from database import init_db

init_db()
from auth import login

from modules.dashboard import render_dashboard
from modules.perfil import render_perfil
from modules.treino_config import render_treino
from modules.objetivos import render_objetivos
from modules.metricas import render_metricas
from modules.plano import render_plano
from modules.treinos_realizados import render_treinos
from modules.biblioteca import render_biblioteca
from modules.admin import render_admin


# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="UltraCoach",
    layout="centered"
)

# 🎨 GLOBAL STYLE (MOBILE + CORES)
st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
}

/* BOTÕES */
.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 48px;
    font-size: 16px;
}

/* CARDS */
.card {
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: white;
}

/* CORES */
.green {background-color:#1e7f4f;}
.red {background-color:#a83232;}
.blue {background-color:#2b5da8;}
.yellow {background-color:#b59b2a;}
.gray {background-color:#444;}
</style>
""", unsafe_allow_html=True)

init_db()


def logout():
    st.session_state.clear()
    st.rerun()


# =========================
# LOGIN
# =========================
if "user_id" not in st.session_state:
    login()
    st.stop()

user_id = st.session_state["user_id"]
role = st.session_state["role"]


# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.title("UltraCoach")

    if role == "admin":
        menu = st.radio("Menu", ["Atletas", "Biblioteca"])
    else:
        menu = st.radio("Menu", [
            "Dashboard",
            "Perfil",
            "Treino",
            "Objetivos",
            "Métricas",
            "Plano",
            "Treinos Realizados",
            "Biblioteca"
        ])

    st.divider()

    if st.button("Logout"):
        logout()


# =========================
# ROUTING
# =========================
if role == "admin":
    render_admin(menu)

else:
    if menu == "Dashboard":
        render_dashboard(user_id)

    elif menu == "Perfil":
        render_perfil(user_id)

    elif menu == "Treino":
        render_treino(user_id)

    elif menu == "Objetivos":
        render_objetivos(user_id)

    elif menu == "Métricas":
        render_metricas(user_id)

    elif menu == "Plano":
        render_plano(user_id)

    elif menu == "Treinos Realizados":
        render_treinos(user_id)

    elif menu == "Biblioteca":
        render_biblioteca()
