import streamlit as st
from view import View
import time

class PerfilClienteUI:
    def main():
        st.header("Meus Dados")
        op = View.cliente_listar_id(st.session_state["usuario_id"])
        
        nome = st.text_input("Informe o novo nome", op.get_nome(), key="perfil_nome")
        email = st.text_input("Informe o novo e-mail", op.get_email(), key="perfil_email")
        fone = st.text_input("Informe o novo fone", op.get_fone(), key="perfil_fone")
        senha = st.text_input("Informe a nova senha", op.get_senha(), type="password", key="perfil_senha")
        observacoes = st.text_area("Observações (Ex: alergias, necessidades especiais)", op.get_observacoes(), key="perfil_observacoes")

        if st.button("Atualizar", key="perfil_botao"):
            try:
                id = op.get_id()
                View.cliente_atualizar(id, nome, email, fone, senha, observacoes)
                
                st.success("Cliente atualizado com sucesso")
                time.sleep(1)
                st.rerun()
            except ValueError as e:
                st.error(f"Erro ao atualizar: {e}")