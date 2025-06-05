import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.studente import Studente
from src.utils.file_handler import FileHandler
from src.utils.input_validator import InputValidator
from src.views.console_view import ConsoleView
from colorama import init
from src.utils.database_updater import DatabaseUpdater

def main():
    init()  # Inizializza colorama
    file_handler = FileHandler("registro.txt")
    view = ConsoleView()
    validator = InputValidator()

    while True:
        scelta = view.mostra_menu()
        if scelta == "0":
            print("👋 Arrivederci!")
            break
            
        elif scelta == "1":
            studenti = file_handler.load_students()
            view.stampa_studenti(studenti)
            
        elif scelta == "2":
            # Aggiunta nuovo studente
            nuovo_studente = view.richiedi_dati_studente(validator)
            if nuovo_studente:
                studenti = file_handler.load_students()
                # Verifica se la matricola esiste già
                if any(s.matricola == nuovo_studente.matricola for s in studenti):
                    print("❌ Errore: Matricola già esistente!")
                    continue
                studenti.append(nuovo_studente)
                if file_handler.save_students(studenti):
                    print(f"✅ Studente {nuovo_studente.nome} {nuovo_studente.cognome} aggiunto con successo!")
                    
        elif scelta == "3":
            # Aggiunta voto
            studenti = file_handler.load_students()
            if not studenti:
                print("❌ Nessuno studente presente nel registro!")
                continue
                
            matricola = input("Inserisci la matricola dello studente: ").strip()
            studente = next((s for s in studenti if s.matricola == matricola), None)
            if not studente:
                print("❌ Studente non trovato!")
                continue
                
            voto_str = input("Inserisci il nuovo voto (18-30): ").strip()
            if validator.valida_voto(voto_str):
                voto = int(voto_str)
                studente.voti.append(voto)
                if file_handler.save_students(studenti):
                    print(f"✅ Voto {voto} aggiunto con successo!")
            else:
                print("❌ Voto non valido!")
                
        elif scelta == "4":
            # Cancellazione studente
            studenti = file_handler.load_students()
            if not studenti:
                print("❌ Nessuno studente presente nel registro!")
                continue
                
            matricola = input("Inserisci la matricola dello studente da cancellare: ").strip()
            studente = next((s for s in studenti if s.matricola == matricola), None)
            if not studente:
                print("❌ Studente non trovato!")
                continue
                
            conferma = input(f"⚠️ Sei sicuro di voler cancellare lo studente {studente.nome} {studente.cognome}? (s/N): ").strip().lower()
            if conferma == 's':
                studenti.remove(studente)
                if file_handler.save_students(studenti):
                    print("✅ Studente cancellato con successo!")
            else:
                print("Operazione annullata.")
        
        elif scelta == "5":
            print("\nControllo matricole nel database...")
            updater = DatabaseUpdater(file_handler, validator)
            n_aggiornamenti, modifiche = updater.aggiorna_matricole()
            
            if n_aggiornamenti > 0:
                print(f"\nMatricole aggiornate: {n_aggiornamenti}")
                print("\nRiepilogo modifiche:")
                for m in modifiche:
                    print(f"- {m['nome']} {m['cognome']}: {m['vecchia']} -> {m['nuova']}")
            else:
                print("✅ Nessuna matricola da aggiornare!")
        
        else:
            print("⚠️ Scelta non valida!")

if __name__ == "__main__":
    main()