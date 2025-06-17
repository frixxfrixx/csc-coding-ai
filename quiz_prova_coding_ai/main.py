"""
Punto di ingresso del Quiz a scelta multipla.

Avvia l'interfaccia web del quiz utilizzando Streamlit.

:author: frixx & ai
:created: 2025-06-17
"""

import os
import subprocess
import webbrowser
from time import sleep

def main():
    """
    Avvia l'applicazione web e apre il browser.
    """
    # Ottiene il percorso assoluto della directory corrente
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Avvia il server Streamlit in background
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "quiz_streamlit.py"],
        cwd=current_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Aspetta un momento per permettere al server di avviarsi
    sleep(2)
    
    # Apri il browser all'URL locale
    webbrowser.open('http://localhost:8501')
    
    print("✨ Quiz avviato! Se il browser non si apre automaticamente, visita: http://localhost:8501")
    print("Per terminare il quiz, chiudi questa finestra.")
    
    try:
        # Mantieni il processo attivo
        streamlit_process.wait()
    except KeyboardInterrupt:
        # Gestisce la chiusura pulita con Ctrl+C
        streamlit_process.terminate()
        print("\n👋 Grazie per aver giocato!")

if __name__ == "__main__":
    main()