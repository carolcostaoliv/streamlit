import streamlit as st
from view import View
import pandas as pd

class VerServicoUI:
    def main():
        st.header("Meus Serviços")
        
        if "usuario_id" not in st.session_state:
            st.error("Você precisa estar logado para ver seus serviços.")
            return
            
        id_cliente_logado = st.session_state["usuario_id"]
        meus_agendamentos = View.horario_filtrar_cliente(id_cliente_logado)
        
        if len(meus_agendamentos) == 0:
            st.info("Você ainda não possui serviços agendados.")
            return
            
        lista_formatada = []
        for h in meus_agendamentos:
            servico_nome = "Não definido"
            if h.get_id_servico() is not None and h.get_id_servico() != 0:
                servico = View.servico_listar_id(h.get_id_servico())
                if servico:
                    servico_nome = servico.get_descricao()
            
            profissional_nome = "Profissional Não Encontrado"
            profissional_id = h.get_id_profissional()
            if profissional_id is not None and profissional_id != 0:
                profissional = View.profissional_listar_id(profissional_id) 
                if profissional:
                    profissional_nome = profissional.get_nome()

            lista_formatada.append({
                "Data": h.get_data().strftime("%d/%m/%Y %H:%M"), 
                "Status": h.get_confirmado(),
                "Serviço": servico_nome, 
                "Profissional": profissional_nome, 
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
                    "Data": st.column_config.DatetimeColumn("Data", format="DD/MM/YYYY HH:mm")
                }
            ) 
        else:
            st.write("Nenhum serviço agendado.")