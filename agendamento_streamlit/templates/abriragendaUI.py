import streamlit as st
from view import View 
from datetime import datetime, timedelta
import time

class AbrirAgendaUI:
    def main():
        st.header("Abrir Minha Agenda")
        data = st.text_input("Informe a data")
        hora_inicio = st.text_input("Horário inicial")
        hora_fim = st.text_input("Horário final ")
        intervalo = st.text_input("Intervalo entre os horários")
        if "usuario_id" not in st.session_state:
             st.error("Profissional não cadastrado")
             return
        if st.button("Abrir Agenda"):
            try:
                id_profissional = st.session_state["usuario_id"]
                intervalo_min = int(intervalo) 
                intervalo_delta = timedelta(minutes=intervalo_min)
                horario_atual = datetime.strptime(f"{data} {hora_inicio}", "%d/%m/%Y %H:%M")
                horario_final = datetime.strptime(f"{data} {hora_fim}", "%d/%m/%Y %H:%M") 
                horarios_inseridos = 0
                while horario_atual <= horario_final:
                    View.horario_inserir(horario_atual, False, None, None, id_profissional)
                    horario_atual += intervalo_delta
                    horarios_inseridos += 1
                if horarios_inseridos > 0:
                    st.success(f" {horarios_inseridos} horários inseridos com sucesso!")
                    time.sleep(4) 
                    st.rerun()
                else:
                    st.warning("Nenhum horário foi inserido")
            except ValueError:
                st.error("Hora ou intervalo inválido")
            except Exception as e:
                st.error(f"Erro: {e}")