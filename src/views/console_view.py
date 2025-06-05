from colorama import Fore, Style
from tabulate import tabulate
from src.models.studente import Studente
from src.utils.matematici import calcola_media
from typing import List, Optional

class ConsoleView:
    @staticmethod
    def mostra_menu() -> str:
        print(f"\n{Fore.CYAN}=== Registro Studenti ==={Fore.RESET}")
        print("[1] Visualizza lista studenti")
        print("[2] Aggiungi studente")
        print("[3] Aggiungi voto")
        print("[4] Cancella studente")
        print("[0] Esci")
        return input("\nScelta: ").strip()

    @staticmethod
    def stampa_studenti(studenti: List[Studente]):
        # Ordina gli studenti per matricola
        studenti_ordinati = sorted(studenti, key=lambda s: s.matricola)
        
        headers = ["Matricola", "Nome", "Cognome", "Media Voti"]
        rows = []
        for studente in studenti_ordinati:  # Usa la lista ordinata invece di quella originale
            media = calcola_media(studente.voti)
            color = (Fore.RED if media < 24 else 
                    Fore.GREEN if media >= 27 else 
                    Fore.RESET)
            rows.append([
                studente.matricola,
                studente.nome,
                studente.cognome,
                f"{color}{media:.2f}{Fore.RESET}"
            ])
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        
    @staticmethod
    def richiedi_dati_studente(validator: 'InputValidator') -> Optional[Studente]:
        """Richiede all'utente i dati per un nuovo studente"""
        # Richiesta matricola
        while True:
            matricola = input("Inserisci la matricola (5-10 cifre): ").strip()
            if validator.valida_matricola(matricola):
                break
            print("❌ Matricola non valida!")
            
        # Richiesta nome
        while True:
            nome = input("Nome: ").strip()
            if validator.valida_nome(nome):
                break
            print("❌ Il nome non può essere vuoto!")
            
        # Richiesta cognome
        while True:
            cognome = input("Cognome: ").strip()
            if validator.valida_nome(cognome):
                break
            print("❌ Il cognome non può essere vuoto!")
            
        # Richiesta voti iniziali (opzionale)
        voti = []
        voti_input = input("Inserisci i voti separati da virgola (opzionale): ").strip()
        if voti_input:
            try:
                for v in voti_input.split(","):
                    if validator.valida_voto(v.strip()):
                        voti.append(int(v.strip()))
            except ValueError:
                print("⚠️ Alcuni voti non validi sono stati ignorati")
                
        return Studente(matricola, nome, cognome, voti)