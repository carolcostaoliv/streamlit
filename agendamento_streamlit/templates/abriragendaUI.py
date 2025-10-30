import streamlit as st
from view import View 
from datetime import datetime, timedelta
import time

class AbrirAgendaUI:
    def main():
        st.header("Abrir Minha Agenda")
        
        hoje_str = datetime.now().strftime("%d/%m/%Y")
        data = st.text_input("Informe a data (ex: 31/10/2025)", hoje_str)
        hora_inicio = st.text_input("Horário inicial (ex: 09:00)", "09:00")
        hora_fim = st.text_input("Horário final (ex: 18:00)", "18:00")
        intervalo = st.text_input("Intervalo em minutos (ex: 30)", "30")
        
        if "usuario_id" not in st.session_state:
             st.error("Profissional não cadastrado")
             return
             
        if st.button("Abrir Agenda"):
            try:
                id_profissional = st.session_state["usuario_id"]
                intervalo_min = int(intervalo) 
                if intervalo_min <= 0:
                     raise ValueError("O intervalo deve ser um número positivo de minutos")
                     
                intervalo_delta = timedelta(minutes=intervalo_min)
                horario_atual = datetime.strptime(f"{data} {hora_inicio}", "%d/%m/%Y %H:%M")
                horario_final = datetime.strptime(f"{data} {hora_fim}", "%d/%m/%Y %H:%M") 
                
                if horario_final < horario_atual:
                    raise ValueError("O horário final deve ser depois do horário inicial")

                horarios_inseridos = 0
                while horario_atual <= horario_final:
                    View.horario_inserir(horario_atual, False, None, None, id_profissional)
                    horario_atual += intervalo_delta
                    horarios_inseridos += 1
                    
                if horarios_inseridos > 0:
                     st.success(f" {horarios_inseridos} horários inseridos com sucesso!")
                     time.sleep(2) 
                     st.rerun()
                else:
                     st.warning("Nenhum horário foi inserido (verifique os horários inicial e final)")
            
            except ValueError as e:
                st.error(f"Erro ao abrir agenda: {e}")
            except Exception as e:
                st.error(f"Erro inesperado: {e}")
