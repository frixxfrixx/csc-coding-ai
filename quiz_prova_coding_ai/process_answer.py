"""
Gestisce il processamento delle risposte nel quiz.
"""

import streamlit as st
from models import Domanda
from score_calculator import calculate_score

def process_answer(question: Domanda, answer: str, elapsed_time: float):
    """Processa la risposta dell'utente."""
    points = calculate_score(
        is_correct=answer == question.corretta,
        tempo=elapsed_time,
        timeout=st.session_state.timeout
    )
    
    # Aggiorna statistiche
    if answer is None:
        st.session_state.stats["saltate"] += 1
    elif answer == question.corretta:
        st.session_state.stats["corrette"] += 1
    else:
        st.session_state.stats["errate"] += 1
    
    st.session_state.stats["tempi"].append(elapsed_time)
    st.session_state.score += points
    st.session_state.current_question_index += 1
    st.session_state.start_time = st.session_state.start_time
    
    st.rerun()
