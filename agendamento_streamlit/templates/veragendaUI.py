import streamlit as st
from view import View 
import pandas as pd

class VerAgendaUI:
    def main():
        st.header("Minha Agenda")
        if "usuario_id" not in st.session_state:
            st.error("Profissional não está cadastrado")
            return
        
        id_profissional = st.session_state["usuario_id"]
        horarioss = View.horario_filtrar_profissional(id_profissional)
        
        if len(horarioss) == 0:
            st.write("Nenhum horário cadastrado na agenda")
            return
            
        lista_formatada = []
        for h in horarioss:
            cliente_nome = "Disponível"
            if h.get_id_cliente() is not None and h.get_id_cliente() != 0:
                cliente = View.cliente_listar_id(h.get_id_cliente())
                if cliente:
                    cliente_nome = cliente.get_nome()
            
            servico_nome = "Nenhum"
            if h.get_id_servico() is not None and h.get_id_servico() != 0:
                servico = View.servico_listar_id(h.get_id_servico())
                if servico:
                    servico_nome = servico.get_descricao()
            
            lista_formatada.append({
                "Data": h.get_data().strftime("%d/%m/%Y %H:%M"), 
                "Status": h.get_confirmado(), 
                "Cliente": cliente_nome, 
                "Serviço": servico_nome,
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
            st.write("Nenhum horário encontrado")
