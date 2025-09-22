import streamlit as st
import pandas as pd
import time
from view import View

class ManterServicosUI:

    def main():
        st.header("Cadastro de Servicos")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterServicosUI.listar()
        with tab2: ManterServicosUI.inserir()
        with tab3: ManterServicosUI.atualizar()
        with tab4: ManterServicosUI.excluir()

    def listar():
        servicos = View.servicos_listar()
        if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
        else:
            list_dic = []
            for obj in servicos: list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df)

    def inserir():
        descricao = st.text_input("Informe a descricao")
        valor = st.number_input("Informe o valor")
        if st.button("Inserir"):
            View.Servico_inserir(descricao, valor)
            st.success("serviço inserido com sucesso")
            time.sleep(2)
            st.rerun()

    def atualizar():
        servicos = View.servicos_listar()
        if len(servicos) == 0: st.write("Nenhum Serviço cadastrado")
        else:
            op = st.selectbox("Atualização de serviços", servicos)
            descricao = st.text_input("Nova descricao", op.get_descricao())
            valor = st.number_input("Novo valor", op.get_valor())
    
            if st.button("Atualizar"):
                id = op.get_id()
                View.servico_atualizar(id, descricao, valor)
                st.success("serviço atualizado com sucesso")
                time.sleep(2)
                st.rerun()

    def excluir():
        servicos = View.servicos_listar()
        if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
        else:
            op = st.selectbox("Exclusão de serviços", servicos)
            if st.button("Excluir"):
                id = op.get_id()
                View.Servico_excluir(id)
                st.success("serviço excluído com sucesso")
                time.sleep(2)
                st.rerun()



