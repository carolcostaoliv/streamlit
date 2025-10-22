import streamlit as st
import time
from view import View

class AlterarSenhaUI:
    def main():
        st.header("Alterar Senha do Admin")
        id_admin = st.session_state["usuario_id"]
        admin = View.cliente_listar_id(id_admin)
        st.write(f"Email: {admin.get_email()}")
        nova_senha = st.text_input("Nova senha", type="password")
        confirmar = st.text_input("Confirmar nova senha", type="password")

        if st.button("Atualizar senha"):
            if nova_senha.strip() == "" or confirmar.strip() == "":
                st.warning("Preencha os dois espaços com a mesma senha")
                time.sleep(4)
            elif nova_senha != confirmar:
                st.error("Senhas diferentes")
                time.sleep(4)
            else:
                View.cliente_atualizar(admin.get_id(), admin.get_nome(), admin.get_email(), admin.get_fone(), nova_senha)
                st.success("Senha atualizada com sucesso")
                time.sleep(4)