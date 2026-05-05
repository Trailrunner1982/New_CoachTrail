import streamlit as st
from database import init_db
from auth import login

from modules.perfil import render_perfil
from modules.treino_config import render_treino
from modules.objetivos import render_objetivos
from modules.metricas import render_metricas
from modules.plano import render_plano
from modules.treinos_realizados import render_treinos
from modules.biblioteca import render_biblioteca
from modules.admin import render_admin


init_db()


def logout():
    st.session_state.clear()
    st.rerun()


# LOGIN
if "user_id" not in st.session_state:
    login()
    st.stop()


role = st.session_state["role"]
user_id = st.session_state["user_id"]


# SIDEBAR
if role == "admin":
    menu = st.sidebar.radio("Menu", ["Atletas", "Biblioteca"])
else:
    menu = st.sidebar.radio("Menu", [
        "Dashboard",
        "Perfil",
        "Treino",
        "Objetivos",
        "Métricas",
        "Plano",
        "Treinos Realizados",
        "Biblioteca"
    ])

if st.sidebar.button("Logout"):
    logout()


# ROUTING
if role == "admin":
    render_admin(menu)
else:
    if menu == "Perfil":
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
    else:
        st.write("Dashboard em construção")
