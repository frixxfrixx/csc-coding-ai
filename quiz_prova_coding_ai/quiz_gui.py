"""
Interfaccia grafica per il Quiz a scelta multipla.
Implementa le tre schermate principali:
1. Schermata di benvenuto con selezione difficoltà
2. Schermata del quiz con domanda e risposte
3. Schermata di riepilogo finale

Autore: Your Name
Data: 2025-06-17
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
from typing import Optional, Dict, List

from models import Domanda, QuizSession
from config import DIFFICULTY_SETTINGS
from data_loader import load_questions
from score_calculator import calculate_score

# Costanti per i colori e lo stile
COLORS = {
    'primary': '#2196F3',    # Blu principale
    'secondary': '#FFC107',  # Giallo per evidenziazioni
    'success': '#4CAF50',    # Verde per risposte corrette
    'error': '#F44336',      # Rosso per risposte errate
    'background': '#FFFFFF', # Sfondo bianco
    'text': '#212121',       # Testo principale
}

class QuizApp:
    """Classe principale dell'applicazione Quiz."""
    
    def __init__(self, root):
        """Inizializza l'applicazione."""
        self.root = root
        self.root.title("Quizzone Bellissimo")
        self.root.geometry("800x600")
        self.root.configure(bg=COLORS['background'])
        
        # Stato dell'applicazione
        self.session: Optional[QuizSession] = None
        self.current_question: Optional[Domanda] = None
        self.timer_id = None
        self.time_left = 0
        
        # Configura stili
        self.setup_styles()
        
        # Mostra schermata iniziale
        self.setup_welcome_screen()
    
    def setup_styles(self):
        """Configura gli stili personalizzati per i widget."""
        style = ttk.Style()
        
        # Stile per i pulsanti principali
        style.configure(
            "Primary.TButton",
            background=COLORS['primary'],
            foreground=COLORS['text'],
            font=('Helvetica', 12),
            padding=10
        )
        
        # Stile per le etichette dei titoli
        style.configure(
            "Title.TLabel",
            font=('Helvetica', 24, 'bold'),
            foreground=COLORS['text'],
            background=COLORS['background'],
            padding=20
        )

    def clear_screen(self):
        """Pulisce tutti i widget dalla finestra."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def setup_welcome_screen(self):
        """Crea e mostra la schermata di benvenuto."""
        self.clear_screen()
        
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        # Titolo
        title = ttk.Label(
            main_frame, 
            text="Benvenuto\nal\nQUIZZONE BELLISSIMO",
            style="Title.TLabel",
            justify='center'
        )
        title.pack(pady=20)
        
        # Sottotitolo per la selezione della difficoltà
        subtitle = ttk.Label(
            main_frame,
            text="Scegli la difficoltà",
            font=('Helvetica', 16),
            padding=10
        )
        subtitle.pack(pady=20)
        
        # Frame per i pulsanti della difficoltà
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=20)
        
        # Pulsanti per ogni livello di difficoltà
        difficulties = [
            ("FACILE", 1),
            ("MEDIA", 2),
            ("DIFFICILE", 3)
        ]
        
        for text, level in difficulties:
            btn = ttk.Button(
                buttons_frame,
                text=f"{text} ({DIFFICULTY_SETTINGS[level][0]} domande, {DIFFICULTY_SETTINGS[level][1]}s)",
                style="Primary.TButton",
                command=lambda l=level: self.start_quiz(l)
            )
            btn.pack(pady=5, padx=10, fill='x')

    def start_quiz(self, difficulty: int):
        """Avvia una nuova sessione quiz con la difficoltà selezionata."""
        num_questions, timeout = DIFFICULTY_SETTINGS[difficulty]
        
        try:
            # Carica le domande
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "questions.json")
            questions = load_questions(file_path)
            
            # Mescola e seleziona le domande
            random.shuffle(questions)
            selected_questions = questions[:num_questions]
            
            # Inizializza la sessione
            self.session = QuizSession(
                domande=selected_questions,
                timeout=timeout
            )
            
            # Mostra la prima domanda
            self.show_question()
            
        except Exception as e:
            messagebox.showerror(
                "Errore",
                f"Errore nel caricamento delle domande: {e}"
            )
            self.setup_welcome_screen()

    def show_question(self):
        """Mostra la schermata della domanda corrente."""
        self.current_question = self.session.next_question()
        if not self.current_question:
            self.show_summary()
            return
        
        self.clear_screen()
        
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        # Frame superiore per timer e punteggio
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='x', pady=(0, 20))
        
        # Timer
        self.timer_label = ttk.Label(
            info_frame,
            text=f"Tempo: {self.session.timeout}s",
            font=('Helvetica', 12)
        )
        self.timer_label.pack(side='left')
        
        # Punteggio
        score_label = ttk.Label(
            info_frame,
            text=f"Punteggio: {self.session.punteggio}",
            font=('Helvetica', 12)
        )
        score_label.pack(side='right')
        
        # Testo della domanda
        question_text = ttk.Label(
            main_frame,
            text=self.current_question.testo,
            font=('Helvetica', 14),
            wraplength=600,
            justify='center'
        )
        question_text.pack(pady=20)
        
        # Frame per le opzioni di risposta
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill='both', expand=True)
        
        # Pulsanti per le opzioni
        for letter, text in self.current_question.opzioni.items():
            btn = ttk.Button(
                options_frame,
                text=f"{letter}. {text}",
                style="Primary.TButton",
                command=lambda ans=letter: self.answer_question(ans)
            )
            btn.pack(pady=5, padx=10, fill='x')
        
        # Avvia il timer
        self.time_left = self.session.timeout
        self.update_timer()

    def update_timer(self):
        """Aggiorna il timer della domanda corrente."""
        if self.time_left > 0:
            self.timer_label.configure(text=f"Tempo: {self.time_left}s")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.answer_question(None)  # Tempo scaduto

    def answer_question(self, answer: Optional[str]):
        """Gestisce la risposta dell'utente."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        
        elapsed_time = self.session.timeout - self.time_left
        points, is_correct, timeout = self.session.record_answer(
            self.current_question,
            answer,
            elapsed_time
        )
        
        # Mostra feedback
        if timeout:
            messagebox.showinfo("Tempo scaduto!", "Tempo esaurito per questa domanda.")
        elif is_correct:
            messagebox.showinfo("Corretto!", f"Hai guadagnato {points} punti!")
        else:
            messagebox.showinfo("Sbagliato!", 
                              f"La risposta corretta era {self.current_question.corretta}. "
                              f"Hai perso {abs(points)} punti.")
        
        # Passa alla prossima domanda
        self.show_question()

    def show_summary(self):
        """Mostra la schermata di riepilogo finale."""
        self.clear_screen()
        
        # Frame principale
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        # Titolo
        title = ttk.Label(
            main_frame,
            text="Quiz Completato!",
            style="Title.TLabel"
        )
        title.pack(pady=20)
        
        # Statistiche
        stats_frame = ttk.LabelFrame(main_frame, text="Le tue statistiche", padding=10)
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        stats = [
            ("Punteggio Totale", self.session.punteggio),
            ("Risposte Corrette", self.session.stats["corrette"]),
            ("Risposte Errate", self.session.stats["errate"]),
            ("Domande Saltate", self.session.stats["saltate"]),
            ("Tempo Medio (s)", sum(self.session.stats["tempi"]) / len(self.session.stats["tempi"]) 
             if self.session.stats["tempi"] else 0)
        ]
        
        for label, value in stats:
            row = ttk.Frame(stats_frame)
            row.pack(fill='x', pady=2)
            
            ttk.Label(row, text=label).pack(side='left')
            ttk.Label(row, text=str(round(value, 2))).pack(side='right')
        
        # Pulsanti finali
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=20)
        
        ttk.Button(
            buttons_frame,
            text="Gioca ancora",
            style="Primary.TButton",
            command=self.setup_welcome_screen
        ).pack(side='left', padx=5, expand=True)
        
        ttk.Button(
            buttons_frame,
            text="Esci",
            style="Primary.TButton",
            command=self.root.quit
        ).pack(side='right', padx=5, expand=True)

def main():
    """Funzione principale per avviare l'applicazione."""
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
