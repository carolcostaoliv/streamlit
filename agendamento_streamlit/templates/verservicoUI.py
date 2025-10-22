import streamlit as st
from view import View
import pandas as pd

class VerServicoUI:
    def main():
        st.header("Meus Serviços")
        if "usuario_id" not in st.session_state:
            st.error("Cliente não está cadastrado")
            return
        id_cliente_logado = st.session_state["usuario_id"]
        meus_horarios = View.horario_filtrar_cliente(id_cliente_logado)
        if len(meus_horarios) == 0:
            st.info("Nenhum serviço agendado")
            return
        lista_formatada = []
        for h in meus_horarios:
            servico_nome = "Não definido"
            if h.get_id_servico() is not None:
                servico = View.servico_listar_id(h.get_id_servico())
                if servico:
                    servico_nome = servico.get_descricao()
            profissional_nome = "Não definido"
            if h.get_id_profissional() is not None:
                prof = View.profissional_listar_id(h.get_id_profissional())
                if prof:
                    profissional_nome = prof.get_nome()
            lista_formatada.append({"Data": h.get_data().strftime("%d/%m/%Y %H:%M"), "Confirmado": "Sim" if h.get_confirmado() else "Não", "Serviço": servico_nome, "Profissional": profissional_nome,})
        if len(lista_formatada) > 0:
            df = pd.DataFrame(lista_formatada)
            st.dataframe(df, use_container_width=True, hide_index=True) 
        else:
            st.write("Nenhum serviço agendado.")