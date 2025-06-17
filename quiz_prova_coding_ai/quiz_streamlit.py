"""
Interfaccia web per il Quiz a scelta multipla utilizzando Streamlit.
Implementa le tre schermate principali:
1. Schermata di benvenuto con selezione difficoltà
2. Schermata del quiz con domanda e risposte
3. Schermata di riepilogo finale

:author: frixx & ai
:created: 2025-06-17
"""

import streamlit as st
import json
import os
import random
from datetime import datetime, timedelta

from models import Domanda, QuizSession
from config import DIFFICULTY_SETTINGS
from data_loader import load_questions
from score_calculator import calculate_score

# Configurazione della pagina
st.set_page_config(
    page_title="Quizzone Bellissimo",
    page_icon="✨",
    layout="centered"
)

# Stili CSS personalizzati
st.markdown("""
    <style>
    .main {
        background-color: #FFFFFF;
    }
    .stButton>button {
        width: 100%;
        background-color: #2196F3;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
    }
    .success {
        color: #4CAF50;
    }
    .error {
        color: #F44336;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Inizializza o resetta lo stato della sessione."""
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'stats' not in st.session_state:
        st.session_state.stats = {
            "corrette": 0,
            "errate": 0,
            "saltate": 0,
            "tempi": []
        }
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'timeout' not in st.session_state:
        st.session_state.timeout = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None

def load_and_start_quiz(difficulty: int):
    """Carica le domande e avvia una nuova sessione quiz."""
    num_questions, timeout = DIFFICULTY_SETTINGS[difficulty]
    
    try:
        # Carica le domande
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "questions.json")
        all_questions = load_questions(file_path)
        
        # Mescola e seleziona le domande
        random.shuffle(all_questions)
        selected_questions = all_questions[:num_questions]
        
        # Inizializza la sessione
        st.session_state.quiz_started = True
        st.session_state.current_question_index = 0
        st.session_state.score = 0
        st.session_state.questions = selected_questions
        st.session_state.timeout = timeout
        st.session_state.stats = {
            "corrette": 0,
            "errate": 0,
            "saltate": 0,
            "tempi": []
        }
        st.session_state.start_time = datetime.now()
        
    except Exception as e:
        st.error(f"Errore nel caricamento delle domande: {e}")
        st.session_state.quiz_started = False

def show_welcome_screen():
    """Mostra la schermata di benvenuto."""
    st.title("Benvenuto al QUIZZONE BELLISSIMO! ✨")
    
    st.markdown("### Scegli la difficoltà")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("FACILE 😊\n5 domande, 15s"):
            load_and_start_quiz(1)
    
    with col2:
        if st.button("MEDIA 🤔\n10 domande, 10s"):
            load_and_start_quiz(2)
    
    with col3:
        if st.button("DIFFICILE 😱\n15 domande, 5s"):
            load_and_start_quiz(3)

def show_question():
    """Mostra la domanda corrente."""
    if st.session_state.current_question_index >= len(st.session_state.questions):
        show_summary()
        return
    
    question = st.session_state.questions[st.session_state.current_question_index]
    
    # Calcola il tempo rimanente
    elapsed = datetime.now() - st.session_state.start_time
    remaining = st.session_state.timeout - elapsed.total_seconds()
    
    # Mostra timer e punteggio
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tempo rimanente", f"{max(0, int(remaining))}s")
    with col2:
        st.metric("Punteggio", st.session_state.score)
    
    # Mostra la domanda
    st.markdown(f"### {question.testo}")
    
    # Mostra le opzioni come pulsanti
    for letter, text in question.opzioni.items():
        if st.button(f"{letter}. {text}", key=letter):
            process_answer(question, letter, st.session_state.timeout - remaining)
    
    # Gestione timeout
    if remaining <= 0:
        process_answer(question, None, st.session_state.timeout)

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
        st.warning("⏰ Tempo scaduto!")
    elif answer == question.corretta:
        st.session_state.stats["corrette"] += 1
        st.success(f"✅ Corretto! Hai guadagnato {points} punti!")
    else:
        st.session_state.stats["errate"] += 1
        st.error(f"❌ Sbagliato! La risposta corretta era {question.corretta}")
    
    st.session_state.stats["tempi"].append(elapsed_time)
    st.session_state.score += points
    st.session_state.current_question_index += 1
    st.session_state.start_time = datetime.now()
    
    # Piccola pausa per mostrare il feedback
    st.balloons() if answer == question.corretta else None
    st.rerun()

def show_summary():
    """Mostra il riepilogo finale del quiz."""
    st.title("Quiz Completato! 🎉")
    
    # Statistiche principali
    st.markdown("### Le tue statistiche")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Punteggio Totale", st.session_state.score)
    with col2:
        st.metric("Risposte Corrette", st.session_state.stats["corrette"])
    with col3:
        st.metric("Risposte Errate", st.session_state.stats["errate"])
    
    # Statistiche dettagliate
    st.markdown("### Dettagli")
    tempi = st.session_state.stats["tempi"]
    tempo_medio = sum(tempi) / len(tempi) if tempi else 0
    
    st.markdown(f"""
    - Domande saltate: {st.session_state.stats["saltate"]}
    - Tempo medio di risposta: {tempo_medio:.1f}s
    """)
    
    # Pulsanti finali
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Gioca ancora"):
            st.session_state.quiz_started = False
            st.rerun()
    with col2:
        if st.button("📊 Salva Punteggio"):
            # Qui puoi implementare il salvataggio del punteggio
            st.success("Punteggio salvato!")

def main():
    """Funzione principale dell'applicazione."""
    initialize_session_state()
    
    if not st.session_state.quiz_started:
        show_welcome_screen()
    else:
        show_question()

if __name__ == "__main__":
    main()
