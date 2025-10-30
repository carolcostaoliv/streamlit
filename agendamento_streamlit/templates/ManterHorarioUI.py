import streamlit as st
import pandas as pd
from view import View
import time
from datetime import datetime

class ManterHorarioUI:
    def main():
        st.header("Cadastro de Horários")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterHorarioUI.listar()
        with tab2: ManterHorarioUI.inserir()
        with tab3: ManterHorarioUI.atualizar()
        with tab4: ManterHorarioUI.excluir()

    def listar():
        horarios = View.horario_listar()
        
        if len(horarios) == 0: st.write("Nenhum horário cadastrado no sistema")
        else:
            dic = []
            for obj in horarios:
                cliente = View.cliente_listar_id(obj.get_id_cliente())
                servico = View.servico_listar_id(obj.get_id_servico())
                profissional = View.profissional_listar_id(obj.get_id_profissional())
                
                cliente_nome = "Livre"
                servico_desc = "Livre"
                prof_nome = "Livre (Sem prof.)" 

                if cliente != None: cliente_nome = cliente.get_nome()
                if servico != None: servico_desc = servico.get_descricao()
                if profissional != None: prof_nome = profissional.get_nome()
                    
                dic.append({
                    "id" : obj.get_id(), 
                    "data" : obj.get_data().strftime("%d/%m/%Y %H:%M"), 
                    "confirmado" : obj.get_confirmado(), 
                    "cliente" : cliente_nome, 
                    "serviço" : servico_desc, 
                    "profissional" : prof_nome
                })
            df = pd.DataFrame(dic)
            st.dataframe(df, hide_index=True, use_container_width=True)
            

    def inserir():
        clientes = View.cliente_listar()
        servicos = View.servico_listar()
        profissionais = View.profissional_listar()
        data_hoje = datetime.now().strftime("%d/%m/2025 %H:%M") 
        data = st.text_input("Informe a data e horário do serviço", data_hoje)
        confirmado = st.checkbox("Confirmado")
        cliente = st.selectbox("Informe o cliente (opcional)", clientes, index = None, key="ins_cli")
        servico = st.selectbox("Informe o serviço (opcional)", servicos, index = None, key="ins_ser")
        profissional = st.selectbox("Informe o profissional (obrigatório)", profissionais, index = None, key="ins_pro")
        
        if st.button("Inserir"):
            try:
                id_cliente = None
                id_servico = None
                id_profissional = None
                if cliente != None: id_cliente = cliente.get_id()
                if servico != None: id_servico = servico.get_id()
                if profissional != None: id_profissional = profissional.get_id()
                else:
                    raise ValueError("Um profissional deve ser selecionado")
                    
                View.horario_inserir(datetime.strptime(data, "%d/%m/%Y %H:%M"), confirmado, id_cliente, id_servico, id_profissional)
                st.success("Horário inserido com sucesso")
                time.sleep(2)
                st.rerun()
            except ValueError as e:
                st.error(f"Erro ao inserir horário: {e}")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")
    
    def atualizar():
        horarios = View.horario_listar()
        if len(horarios) == 0: st.write("Nenhum horário cadastrado")
        else:
            clientes = View.cliente_listar()
            servicos = View.servico_listar()
            profissionais = View.profissional_listar()
            
            op = st.selectbox("Atualização de Horários", horarios) 
            data = st.text_input("Informe a nova data e horário do serviço",
                     op.get_data().strftime("%d/%m/%Y %H:%M"))
            confirmado = st.checkbox("Nova confirmação", op.get_confirmado())
            id_cliente = None if op.get_id_cliente() in [0, None] else op.get_id_cliente()
            id_servico = None if op.get_id_servico() in [0, None] else op.get_id_servico()
            id_profissional = None if op.get_id_profissional() in [0, None] else op.get_id_profissional()
            
            idx_cli = next((i for i, c in enumerate(clientes) if c.get_id() == id_cliente), None)
            idx_ser = next((i for i, s in enumerate(servicos) if s.get_id() == id_servico), None)
            idx_pro = next((i for i, p in enumerate(profissionais) if p.get_id() == id_profissional), None)

            cliente = st.selectbox("Informe o novo cliente", clientes, index=idx_cli, key="upd_cli")
            servico = st.selectbox("Informe o novo serviço", servicos, index=idx_ser, key="upd_ser")
            profissional = st.selectbox("Informe o novo profissional", profissionais, index=idx_pro, key="upd_pro")
            
            if st.button("Atualizar"):
                try:
                    id_cliente_novo = None
                    id_servico_novo = None
                    id_profissional_novo = None
                    if cliente != None: id_cliente_novo = cliente.get_id()
                    if servico != None: id_servico_novo = servico.get_id()
                    if profissional != None: id_profissional_novo = profissional.get_id()
                    else:
                        raise ValueError("Um profissional deve ser selecionado")
                    
                    View.horario_atualizar(
                        op.get_id(), 
                        datetime.strptime(data, "%d/%m/%Y %H:%M"), 
                        confirmado, 
                        id_cliente_novo, 
                        id_servico_novo, 
                        id_profissional_novo
                    )
                    st.success("Horário atualizado com sucesso")
                    time.sleep(2)
                    st.rerun()
                except ValueError as e:
                    st.error(f"Erro ao atualizar horário: {e}")
                except Exception as e:
                    st.error(f"Erro inesperado: {e}")

    def excluir():
        horarios_livres = [h for h in View.horario_listar() if h.get_id_cliente() in (None, 0)]
        
        if len(horarios_livres) == 0: 
            st.write("Nenhum horário livre disponível para exclusão.")
            st.write("(Horários já agendados por clientes não podem ser excluídos por aqui)")
        else:
            op = st.selectbox("Exclusão de Horários Livres", horarios_livres)
            
            if st.button("Excluir"):
                try:
                    View.horario_excluir(op.get_id())
                    st.success("Horário excluído com sucesso")
                    time.sleep(2)
                    st.rerun()
                except ValueError as e:
                    st.error(f"Erro ao excluir horário: {e}")
                except Exception as e:
                    st.error(f"Erro inesperado: {e}")

