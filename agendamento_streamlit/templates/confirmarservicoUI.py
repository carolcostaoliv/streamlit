import streamlit as st
from datetime import datetime
from view import View
import time

class ConfirmarServicoUI:
    def main():
        st.header("Confirmar Serviço")
        if "usuario_id" not in st.session_state:
            st.error("Profissional não está cadastrado")
            return
        id_profissional = st.session_state["usuario_id"]
        try:
            horarios_para_confirmar = View.horario_listar_nao_confirmados(id_profissional)
            if len(horarios_para_confirmar) == 0:
                st.info("Todos os serviços já estão confirmados")
                return
            opcoes = []
            for h in horarios_para_confirmar:
                cliente = View.cliente_listar_id(h.get_id_cliente())
                servico = View.servico_listar_id(h.get_id_servico())
                cliente_nome = cliente.get_nome() if cliente else "Cliente não encontrado"
                servico_desc = servico.get_descricao() if servico else "Serviço não encontrado"
                texto_opcao = (f"{h.get_data().strftime('%d/%m/%Y %H:%M')} | "
                               f"Cliente: {cliente_nome} | "
                               f"Serviço: {servico_desc}")
                opcoes.append(texto_opcao)
            st.write("Selecione o agendamento para confirmar:")
            opcao_selecionada = st.selectbox("Agendamentos Pendentes", options=opcoes, label_visibility="collapsed")
            if st.button("Confirmar"):
                indice_selecionado = opcoes.index(opcao_selecionada)
                horario_a_confirmar = horarios_para_confirmar[indice_selecionado]
                View.horario_atualizar(horario_a_confirmar.get_id(), horario_a_confirmar.get_data(), True,horario_a_confirmar.get_id_cliente(), horario_a_confirmar.get_id_servico(), horario_a_confirmar.get_id_profissional())                    
                st.success("Serviço confirmado com sucesso")
                time.sleep(4)
                st.rerun()
        except Exception as e:
            st.error(f"Erro ao buscar horários: {e}")