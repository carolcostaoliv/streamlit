import streamlit as st
import pandas as pd
import time
from view import View

class ManterClienteUI:

    def main():
        st.header("Cadastro de Clientes")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterClienteUI.listar()
        with tab2: ManterClienteUI.inserir()
        with tab3: ManterClienteUI.atualizar()
        with tab4: ManterClienteUI.excluir()

    def listar():
        clientes = View.cliente_listar()
        if len(clientes) == 0: 
            st.write("Nenhum cliente cadastrado")
        else:
            list_dic = []
            for obj in clientes: 
                list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df)

    def inserir():
        nome = st.text_input("Informe o nome", key="inserir_nome")
        email = st.text_input("Informe o e-mail", key="inserir_email")
        fone = st.text_input("Informe o fone", key="inserir_fone")
        senha = st.text_input("Informe a senha", type="password", key="inserir_senha")
        observacoes = st.text_area("Observações (Ex: alergias, necessidades especiais)", key="inserir_observacoes")
        
        if st.button("Inserir", key="inserir_botao"):
            try:
                View.cliente_inserir(nome, email, fone, senha, observacoes)
                st.success("Cliente inserido com sucesso")
                time.sleep(2)
                st.rerun()
            except ValueError as e:
                st.error(f"Erro ao inserir cliente: {e}")

    def atualizar():
        clientes = View.cliente_listar()
        if len(clientes) == 0: 
            st.write("Nenhum cliente cadastrado")
        else:
            # Usar session_state para controlar o cliente selecionado
            if 'cliente_selecionado' not in st.session_state:
                st.session_state.cliente_selecionado = clientes[0].get_id()
            
            op_selecionado = st.selectbox(
                "Atualização de Clientes", 
                clientes,
                key="atualizar_select",
                format_func=lambda x: f"{x.get_id()} - {x.get_nome()} | {x.get_email()}",
                index=next((i for i, c in enumerate(clientes) if c.get_id() == st.session_state.cliente_selecionado), 0)
            )
            
            # Atualizar o session_state quando o selectbox mudar
            if op_selecionado.get_id() != st.session_state.cliente_selecionado:
                st.session_state.cliente_selecionado = op_selecionado.get_id()
                st.rerun()
            
            # Agora usar chaves baseadas no ID do cliente selecionado
            cliente_id = st.session_state.cliente_selecionado
            
            nome = st.text_input(
                "Novo nome", 
                value=op_selecionado.get_nome(), 
                key=f"atualizar_nome_{cliente_id}"
            )
            email = st.text_input(
                "Novo e-mail", 
                value=op_selecionado.get_email(), 
                key=f"atualizar_email_{cliente_id}"
            )
            fone = st.text_input(
                "Novo fone", 
                value=op_selecionado.get_fone(), 
                key=f"atualizar_fone_{cliente_id}"
            )
            senha = st.text_input(
                "Nova senha", 
                value=op_selecionado.get_senha(), 
                type="password", 
                key=f"atualizar_senha_{cliente_id}"
            )
            
            observacoes_value = op_selecionado.get_observacoes() or ""
            observacoes = st.text_area(
                "Observações (Ex: alergias, necessidades especiais)", 
                value=observacoes_value,
                key=f"atualizar_observacoes_{cliente_id}"
            )
            
            if st.button("Atualizar", key=f"atualizar_botao_{cliente_id}"):
                try:
                    View.cliente_atualizar(
                        op_selecionado.get_id(), 
                        nome, email, fone, senha, observacoes
                    )
                    st.success("Cliente atualizado com sucesso")
                    time.sleep(2)
                    st.rerun()
                except ValueError as e:
                    st.error(f"Erro ao atualizar cliente: {e}")

    def excluir():
        clientes = View.cliente_listar()
        if len(clientes) == 0: 
            st.write("Nenhum cliente cadastrado")
        else:
            op = st.selectbox("Exclusão de Clientes", clientes, key="excluir_select")
            if st.button("Excluir", key="excluir_botao"):
                try:
                    id = op.get_id()
                    View.cliente_excluir(id)
                    st.success("Cliente excluído com sucesso")
                    time.sleep(2)
                    st.rerun()
                except ValueError as e: 
                    st.error(f"Erro ao excluir cliente: {e}")