import streamlit as st
from view import View
import time

class AgendarServicoUI:
    def main():
        st.header("Agendar Serviço")
        prof = View.profissional_listar()
        if len(prof) == 0:
            st.write("Nenhum profissional cadastrado")
        else:
            profissional = st.selectbox("Informe o profissional", prof)
            horarios = View.horario_agendar_horario(profissional.get_id())
            if len(horarios) == 0:
                st.write("Nenhum horário disponível")
            else:
                horario = st.selectbox("Informe o horário", horarios)
                servicos = View.servico_listar()
                servico = st.selectbox("Informe o serviço", servicos)
                if st.button("Agendar"):
                    View.horario_atualizar(horario.get_id(), horario.get_data(), False, st.session_state["usuario_id"], servico.get_id(), profissional.get_id())
                    st.success("Horário agendado com sucesso")
                    time.sleep(4)
                    st.rerun()