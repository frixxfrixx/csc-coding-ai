"""
Punto di ingresso del Quiz a scelta multipla.

Permette di avviare il quiz in modalità locale (Tkinter) o web (Streamlit).

:author: frixx & ai
:created: 2025-06-17
"""

import os
import subprocess
import webbrowser
import tkinter as tk
from time import sleep
from quiz_gui import QuizApp

def avvia_modalita_web(current_dir: str):
    """Avvia il quiz in modalità web con Streamlit."""
    # Avvia il server Streamlit in background
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "quiz_streamlit.py"],
        cwd=current_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return streamlit_process

def avvia_modalita_locale():
    """Avvia il quiz in modalità locale con Tkinter."""
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

def chiedi_modalita():
    """Chiede all'utente come vuole avviare il quiz."""
    while True:
        print("\n=== QUIZ - Scegli la modalità ===")
        print("1. Modalità Locale (finestra dedicata)")
        print("2. Modalità Web (browser)")
        print("Q. Esci")
        
        scelta = input("\nScegli un'opzione (1/2/Q): ").strip().upper()
        
        if scelta in ['1', '2', 'Q']:
            return scelta
        print("\nScelta non valida. Riprova.")

def main():
    """
    Punto di ingresso principale dell'applicazione.
    Permette di scegliere tra interfaccia locale o web.
    """
    # Ottiene il percorso assoluto della directory corrente
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    while True:
        scelta = chiedi_modalita()
        
        if scelta == 'Q':
            print("\n👋 Arrivederci!")
            break
            
        elif scelta == '1':
            print("\n🚀 Avvio il quiz in modalità locale...")
            avvia_modalita_locale()
            
        elif scelta == '2':
            print("\n🌐 Avvio il quiz in modalità web...")
              # Avvia il server Streamlit
            streamlit_process = avvia_modalita_web(current_dir)
            
            # Aspetta un momento per permettere al server di avviarsi
            sleep(2)
            
            # Apri il browser all'URL locale
            webbrowser.open('http://localhost:8501')
            
            print("✨ Quiz avviato! Se il browser non si apre automaticamente, visita: http://localhost:8501")
            print("Per terminare il quiz, chiudi questa finestra o premi Ctrl+C")
            
            try:
                # Mantieni il processo attivo
                streamlit_process.wait()
            except KeyboardInterrupt:
                # Gestisce la chiusura pulita con Ctrl+C
                streamlit_process.terminate()
                print("\n👋 Grazie per aver giocato!")
            
            print("\nPremi Invio per tornare al menu principale...")
            input()

if __name__ == "__main__":
    main()