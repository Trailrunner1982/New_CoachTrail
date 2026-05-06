import streamlit as st
from database import init_db
from modules.auth import login
from modules.dashboard import render_dashboard
from modules.admin import render_admin

init_db()

if "logged" not in st.session_state:
    st.session_state["logged"] = False

if not st.session_state["logged"]:
    login()
else:

    role = st.session_state["role"]

    if role == "admin":
        menu = st.sidebar.radio("Menu", ["Admin", "Dashboard"])
    else:
        menu = st.sidebar.radio("Menu", ["Dashboard"])

    if menu == "Dashboard":
        render_dashboard(st.session_state["user_id"])

    if menu == "Admin":
        render_admin()
