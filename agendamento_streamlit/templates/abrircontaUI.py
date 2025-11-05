import streamlit as st
from view import View
import time

class AbrirContaUI:
    def main():
        st.header("Abrir Conta no Sistema")
        nome = st.text_input("Informe o nome", key="abrir_conta_nome")
        email = st.text_input("Informe o e-mail", key="abrir_conta_email")
        fone = st.text_input("Informe o fone", key="abrir_conta_fone")
        senha = st.text_input("Informe a senha", type="password", key="abrir_conta_senha")
        observacoes = st.text_area("Observações (Ex: alergias, necessidades especiais)", key="abrir_conta_observacoes")

        if st.button("Inserir", key="abrir_conta_botao"):
            try:
                View.cliente_inserir(nome, email, fone, senha, observacoes)
                
                st.success("Conta criada com sucesso")
                time.sleep(2)
                st.rerun()
            except ValueError as e:
                st.error(f"Erro ao criar conta: {e}")