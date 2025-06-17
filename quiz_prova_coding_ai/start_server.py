"""
Script per avviare il server Streamlit del Quiz.

:author: frixx & ai
:created: 2025-06-17
"""

import os
import subprocess
import sys
import webbrowser
from time import sleep

def start_streamlit():
    """Avvia il server Streamlit del quiz."""
    # Ottiene il percorso della directory corrente
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, "quiz_streamlit.py")
    
    try:
        # Configura e avvia il processo Streamlit
        process = subprocess.Popen(
            ["streamlit", "run", script_path, "--server.headless", "true"],
            cwd=current_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Attendi l'avvio del server
        sleep(3)
        
        # Apri il browser all'URL locale
        url = "http://localhost:8501"
        webbrowser.open(url)
        
        # Mostra istruzioni
        print("\n" + "="*50)
        print("✨ Quiz avviato!")
        print(f"📝 URL del quiz: {url}")
        print("❌ Per terminare, chiudi questa finestra o premi Ctrl+C")
        print("="*50 + "\n")
        
        # Mantieni il server attivo
        process.wait()
        
    except KeyboardInterrupt:
        print("\n👋 Grazie per aver giocato!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Errore nell'avvio del quiz: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_streamlit()
