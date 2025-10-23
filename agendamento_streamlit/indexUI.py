from templates.ClienteUI import ManterClienteUI
from templates.ManterServicoUI import ManterServicoUI
from templates.ManterHorarioUI import ManterHorarioUI
from templates.ManterProfissionalUI import ManterProfissionalUI
from templates.abrircontaUI import AbrirContaUI
from templates.loginUI import LoginUI
from templates.perfilclienteUI import PerfilClienteUI
from templates.perfilprofissionalUI import PerfilProfissionalUI
from templates.veragendaUI import VerAgendaUI
from templates.verservicoUI import VerServicoUI
from templates.abriragendaUI import AbrirAgendaUI
from templates.agendarservicoUI import AgendarServicoUI
from templates.confirmarservicoUI import ConfirmarServicoUI
from templates.alterarsenhaUI import AlterarSenhaUI
from view import View
import streamlit as st

class IndexUI:

    def menu_admin():            
        op = st.sidebar.selectbox("Menu", ["Cadastro de Clientes", "Cadastro de Serviços", "Cadastro de Horários", "Cadastro de Profissionais", "Alterar Senha"])
        if op == "Cadastro de Clientes": ManterClienteUI.main()
        if op == "Cadastro de Serviços": ManterServicoUI.main()
        if op == "Cadastro de Horários": ManterHorarioUI.main()
        if op == "Cadastro de Profissionais": ManterProfissionalUI.main()
        if op == "Alterar Senha": AlterarSenhaUI.main()


    def menu_visitante():
        op = st.sidebar.selectbox("Menu", ["Entrar no Sistema", "Abrir Conta"])
        if op == "Entrar no Sistema": LoginUI.main()
        if op == "Abrir Conta": AbrirContaUI.main()

    def menu_cliente():
        op = st.sidebar.selectbox("Menu", ["Meus Dados", "Agendar Serviço", "Meus Serviços"])
        if op == "Meus Dados":
            PerfilClienteUI.main()
        if op == "Agendar Serviço":
            AgendarServicoUI.main()
        if op == "Meus Serviços": 
            VerServicoUI.main()
        

    def menu_profissional():
        op = st.sidebar.selectbox("Menu", ["Meus Dados", "Abrir Minha Agenda", "Minha Agenda", "Confirmar Serviço"])
        if op == "Meus Dados": PerfilProfissionalUI.main()
        if op == "Abrir Minha Agenda": AbrirAgendaUI.main()
        if op == "Minha Agenda": VerAgendaUI.main()
        if op == "Confirmar Serviço": ConfirmarServicoUI.main()


    def menu_admin():
        op = st.sidebar.selectbox("Menu", ["Cadastro de Clientes", "Cadastro de Serviços", "Cadastro de Horários", "Cadastro de Profissionais"])
        if op == "Cadastro de Clientes": ManterClienteUI.main()
        if op == "Cadastro de Serviços": ManterServicoUI.main()
        if op == "Cadastro de Horários": ManterHorarioUI.main()
        if op == "Cadastro de Profissionais": ManterProfissionalUI.main()

    def sair_do_sistema():
        if st.sidebar.button("Sair"):
            del st.session_state["usuario_id"]
            del st.session_state["usuario_nome"]
            st.rerun()

    def sidebar():
        if "usuario_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            admin = st.session_state["usuario_nome"] == "admin"
            profissional = View.profissional_listar_id(st.session_state["usuario_id"]) != None 
            st.sidebar.write("Bem-vindo(a), " + st.session_state["usuario_nome"])
            if admin: 
                IndexUI.menu_admin()
            elif profissional: 
                IndexUI.menu_profissional()
            else: 
                IndexUI.menu_cliente()
            IndexUI.sair_do_sistema()


    def main():
        View.cliente_criar_admin()
        IndexUI.sidebar()

IndexUI.main()