# import streamlit as st
# import pandas as pd
# import time
# from view import View

# class ManterServicoUI:
#     def main():
#         st.header("Cadastro de Serviços")
#         tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir","Atualizar", "Excluir"])
#         with tab1: ManterServicoUI.listar()
#         with tab2: ManterServicoUI.inserir()
#         with tab3: ManterServicoUI.atualizar()
#         with tab4: ManterServicoUI.excluir()

#     def listar():
#         servicos = View.servico_listar()
#         if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
#         else:
#             list_dic = []
#             for obj in servicos: list_dic.append(obj.to_json())
#             df = pd.DataFrame(list_dic)
#             st.dataframe(df)

#     def inserir():
#         descricao = st.text_input("Informe a descrição")
#         valor = st.number_input("Informe o valor")
#         if st.button("Inserir"):
#             View.servico_inserir(descricao, valor)
#             st.success("Serviço inserido com sucesso")
#             time.sleep(2)
#             st.rerun()

#     def atualizar():
#         servicos = View.servico_listar()
#         if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
#         else:
#             op = st.selectbox("Atualização de serviços", servicos)
#             descricao = st.text_input("Nova descrição", op.get_descricao())
#             valor = st.text_input("Novo valor", op.get_valor())
#             if st.button("Atualizar"):
#                 id = op.get_id()
#                 View.servico_atualizar(id, descricao, valor)
#                 st.success("Serviço atualizado com sucesso")
#                 time.sleep(2)
#                 st.rerun()

#     def excluir():
#         servicos = View.servico_listar()
#         if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
#         else:
#             op = st.selectbox("Exclusão de servicos", servicos)
#             if st.button("Excluir"):
#                 id = op.get_id()
#                 View.servico_excluir(id)
#                 st.success("Serviço excluído com sucesso")
#                 time.sleep(2)
#                 st.rerun()

import streamlit as st
import pandas as pd
from view import View
import time

class ManterServicoUI:
    def main():
        st.header("Cadastro de Serviços")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterServicoUI.listar()
        with tab2: ManterServicoUI.inserir()
        with tab3: ManterServicoUI.atualizar() # <--- O erro estava aqui
        with tab4: ManterServicoUI.excluir()

    def listar():
        servicos = View.servico_listar()
        if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
        else:
            list_dic = []
            for obj in servicos: list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df, hide_index=True, use_container_width=True)

    def inserir():
        descricao = st.text_input("Informe a descrição do serviço")
        # É melhor usar number_input para valores monetários
        valor = st.number_input("Informe o valor (R$)", min_value=0.01, value=50.0, step=1.0, format="%.2f")
        
        if st.button("Inserir"):
            try:
                View.servico_inserir(descricao, valor)
                st.success("Serviço inserido com sucesso")
                time.sleep(2)
                st.rerun()
            except ValueError as e:
                st.error(f"Erro ao inserir serviço: {e}")

    def atualizar():
        # AQUI ESTAVA O ERRO:
        # A lista buscada deve ser a de serviços, não a de profissionais.
        servicos = View.servico_listar() # <--- CORREÇÃO
        
        if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
        else:
            # O selectbox agora usa a lista correta
            op = st.selectbox("Atualização de Serviços", servicos)
            
            # Esta linha agora vai funcionar, pois 'op' é um Servico
            descricao = st.text_input("Nova descrição", op.get_descricao())
            
            # Assumindo que a próxima linha seria para o valor
            valor = st.number_input(
                "Novo valor (R$)", 
                min_value=0.01, 
                value=op.get_valor(), # O objeto Servico tem get_valor()
                step=1.0, 
                format="%.2f"
            )
            
            if st.button("Atualizar"):
                try:
                    View.servico_atualizar(op.get_id(), descricao, valor)
                    st.success("Serviço atualizado com sucesso")
                    time.sleep(2)
                    st.rerun()
                except ValueError as e:
                    st.error(f"Erro ao atualizar serviço: {e}")

    def excluir():
        servicos = View.servico_listar()
        if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
        else:
            op = st.selectbox("Exclusão de Serviços", servicos)
            if st.button("Excluir"):
                try:
                    # NOTA: O PDF não pedia, mas seria bom adicionar na View
                    # uma validação para não excluir serviços já agendados.
                    View.servico_excluir(op.get_id())
                    st.success("Serviço excluído com sucesso")
                    time.sleep(2)
                    st.rerun()
                except ValueError as e:
                    st.error(f"Erro ao excluir serviço: {e}")