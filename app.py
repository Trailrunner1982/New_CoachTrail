import streamlit as st
from database import init_db
from auth import login
from pages.perfil import perfil_page
from pages.objetivos import objetivos_page
from pages.plano import plano_page
from pages.admin import admin_page

init_db()

if "user_id" not in st.session_state:
    login()
    st.stop()

role = st.session_state["role"]
user_id = st.session_state["user_id"]

menu = st.sidebar.selectbox("Menu", [
    "Perfil",
    "Objetivos",
    "Plano",
    "Admin"
])

if menu == "Perfil":
    perfil_page(user_id)

elif menu == "Objetivos":
    objetivos_page(user_id)

elif menu == "Plano":
    plano_page(user_id)

elif menu == "Admin" and role == "admin":
    admin_page()
