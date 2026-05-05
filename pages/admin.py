import streamlit as st
from database import get_conn


def admin_page():
    st.header("Admin - Gestão")

    conn = get_conn()
    c = conn.cursor()

    # =====================
    # CRIAR ATLETA
    # =====================
    st.subheader("Criar Atleta")

    username = st.text_input("Username novo atleta")
    password = st.text_input("Password", type="password")

    if st.button("Criar atleta"):
        try:
            c.execute("""
            INSERT INTO users (username, password, role)
            VALUES (?, ?, 'athlete')
            """, (username, password))
            conn.commit()
            st.success("Atleta criado")
        except:
            st.error("Username já existe")

    # =====================
    # LISTAR ATLETAS
    # =====================
    st.subheader("Atletas")

    c.execute("SELECT id, username FROM users WHERE role='athlete'")
    atletas = c.fetchall()

    for a in atletas:
        col1, col2 = st.columns(2)

        col1.write(a[1])

        if col2.button(f"Apagar {a[1]}"):
            c.execute("DELETE FROM users WHERE id=?", (a[0],))
            conn.commit()
            st.rerun()

    # =====================
    # BIBLIOTECA
    # =====================
    st.subheader("Biblioteca Global")

    titulo = st.text_input("Título")
    tipo = st.selectbox("Tipo", ["video", "artigo"])
    link = st.text_input("Link")
    descricao = st.text_area("Descrição")

    if st.button("Adicionar à biblioteca"):
        c.execute("""
        INSERT INTO biblioteca (titulo, tipo, link, descricao)
        VALUES (?, ?, ?, ?)
        """, (titulo, tipo, link, descricao))
        conn.commit()
        st.success("Adicionado")

    # LISTAR
    st.subheader("Conteúdo existente")

    c.execute("SELECT * FROM biblioteca")
    items = c.fetchall()

    for i in items:
        st.write(f"📌 {i[1]} ({i[2]})")
        st.write(i[3])
        st.write(i[4])
        st.write("---")
