import streamlit as st
from view import View
import pandas as pd

class VerServicoUI:
    def main():
        st.header("Meus Serviços")
        
        if "usuario_id" not in st.session_state:
            st.error("Usuário não está logado ou não foi cadastrado como profissional.")
            return
            
        id_profissional_logado = st.session_state["usuario_id"]
        horarios_do_profissional = View.horario_filtrar_profissional(id_profissional_logado)
        meus_agendamentos = [h for h in horarios_do_profissional if h.get_id_cliente() is not None and h.get_id_cliente() != 0]

        if len(meus_agendamentos) == 0:
            st.info("Nenhum serviço agendado em sua agenda.")
            return
            
        lista_formatada = []
        for h in meus_agendamentos:
            servico_nome = "Não definido"
            if h.get_id_servico() is not None and h.get_id_servico() != 0:
                servico = View.servico_listar_id(h.get_id_servico())
                if servico:
                    servico_nome = servico.get_descricao()
            
            cliente_nome = "Cliente Não Encontrado"
            cliente_id = h.get_id_cliente()
            if cliente_id is not None and cliente_id != 0:
                cliente = View.cliente_listar_id(cliente_id)
                if cliente:
                    cliente_nome = cliente.get_nome()

            lista_formatada.append({
                "Data": h.get_data().strftime("%d/%m/%Y %H:%M"), 
                "Status": h.get_confirmado(),
                "Serviço": servico_nome, 
                "Cliente": cliente_nome,
            })
            
        if len(lista_formatada) > 0:
            df = pd.DataFrame(lista_formatada)
            
            st.dataframe(
                df, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Status": st.column_config.CheckboxColumn(
                        "Confirmado", 
                        default=False,
                        disabled=True 
                    ),
                    "Data": st.column_config.DatetimeColumn("Data")
                }
            ) 
        else:
            st.write("Nenhum serviço agendado.")
