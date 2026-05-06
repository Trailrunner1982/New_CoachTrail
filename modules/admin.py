import streamlit as st
from database import get_conn


def render_admin(menu):
    st.title("Admin")

    conn = get_conn()
    c = conn.cursor()

    # =========================
    # 👥 GESTÃO DE ATLETAS
    # =========================
    if menu == "Atletas":

        st.subheader("Criar novo atleta")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Criar atleta"):
            if new_user and new_pass:
                try:
                    c.execute("""
                    INSERT INTO users (username, password, role)
                    VALUES (?, ?, ?)
                    """, (new_user, new_pass, "athlete"))
                    conn.commit()
                    st.success("Atleta criado com sucesso")
                    st.rerun()
                except:
                    st.error("Username já existe")
            else:
                st.warning("Preenche username e password")

        st.divider()

        st.subheader("Lista de atletas")

        c.execute("SELECT id, username FROM users WHERE role='athlete'")
        atletas = c.fetchall()

        if not atletas:
            st.info("Sem atletas ainda")
            return

        for a in atletas:
            col1, col2 = st.columns([3, 1])

            col1.write(a[1])

            if col2.button("Apagar", key=f"del_{a[0]}"):
                c.execute("DELETE FROM users WHERE id=?", (a[0],))
                conn.commit()
                st.warning("Atleta removido")
                st.rerun()

    # =========================
    # 📚 BIBLIOTECA
    # =========================
    elif menu == "Biblioteca":

        st.subheader("Adicionar conteúdo")

        titulo = st.text_input("Título")
        link = st.text_input("Link (YouTube, artigo, etc)")
        descricao = st.text_area("Descrição")

        if st.button("Adicionar"):
            if titulo and link:
                c.execute("""
                INSERT INTO biblioteca (titulo, link, descricao)
                VALUES (?, ?, ?)
                """, (titulo, link, descricao))
                conn.commit()
                st.success("Conteúdo adicionado")
                st.rerun()
            else:
                st.warning("Título e link obrigatórios")

        st.divider()

        st.subheader("Conteúdos existentes")

        c.execute("SELECT * FROM biblioteca")
        conteudos = c.fetchall()

        for ctt in conteudos:
            st.write(f"**{ctt[1]}**")
            st.write(ctt[2])

            if st.button("Apagar", key=f"lib_{ctt[0]}"):
                c.execute("DELETE FROM biblioteca WHERE id=?", (ctt[0],))
                conn.commit()
                st.warning("Removido")
                st.rerun()
