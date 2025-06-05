"""
Registro Studenti - Sistema di gestione per studenti universitari
==============================================================
Questo programma implementa un registro elettronico che permette di:
- Visualizzare la lista degli studenti con le loro medie
- Aggiungere nuovi studenti
- Aggiungere voti agli studenti esistenti

I dati vengono salvati in formato JSON in un file di testo.
"""

import os  # Modulo per interagire con il sistema operativo
import json  # Modulo per lavorare con dati in formato JSON (JavaScript Object Notation)
from typing import List, Dict, Optional
from colorama import init, Fore, Style
from tabulate import tabulate
from utils_matematici import calcola_media  # Importa la funzione dal nuovo modulo

# Inizializza colorama per i colori nel terminale
init()

# Costanti di configurazione
VOTO_MIN = 18
VOTO_MAX = 30
FILE_ENCODING = 'utf-8'
JSON_INDENT = 2

# Configurazione del percorso del file dati
# ---------------------------------------
# Gets the absolute path of the 'registro.txt' file in the same folder as the script
# __file__ is a special variable that contains the path of the current file
main_dir = os.path.dirname(__file__)  # Gets the directory containing the script
file_path = os.path.join(main_dir, 'registro.txt')  # Composes the complete file path


def leggi_studenti_da_file(percorso_file: str) -> List[Dict]:
    """
    Legge il file JSON e restituisce la lista degli studenti come lista di dizionari.
    
    Args:
        percorso_file: Percorso completo del file JSON da leggere
        
    Returns:
        List[Dict]: Lista di dizionari, ognuno rappresentante uno studente
                   Restituisce lista vuota in caso di errore
    
    Note:
        - Usa encoding='utf-8' per gestire correttamente i caratteri speciali
        - Gestisce due possibili eccezioni:
          * FileNotFoundError: quando il file non esiste
          * JSONDecodeError: quando il file esiste ma non contiene JSON valido    """
    try:
        with open(percorso_file, encoding='utf-8') as file:  # 'with' assicura che il file venga chiuso
            return json.load(file)  # Converte il JSON in una struttura dati Python
    except (json.JSONDecodeError, FileNotFoundError):
        print("❌ Error in JSON file or file not found.")
        return []  # Returns an empty list in case of error


def stampa_studenti(studenti: List[Dict]):
    print("\nElenco studenti:")
    # Prepara e stampa la tabella formattata
    headers = ["Matricola", "Nome", "Cognome", "Media Voti"]
    rows = []
    for studente in studenti:
        matricola = studente.get("matricola", "N/D")  # 'N/D' è il valore predefinito se la chiave non esiste
        nome = studente.get("nome", "N/D")
        cognome = studente.get("cognome", "N/D")
        voti = studente.get("voti", [])  # Lista vuota se la chiave non esiste
        media = calcola_media(voti)
        
        # Colora la media in base al valore
        color = Fore.RED if media < 24 else Fore.GREEN if media >= 27 else Fore.RESET
        rows.append([
            matricola,
            nome,
            cognome,
            f"{color}{media:.2f}{Fore.RESET}"
        ])
    
    print(tabulate(rows, headers=headers, tablefmt="grid"))


def esegui_processo(percorso_file: str):
    
    studenti = leggi_studenti_da_file(percorso_file)  # First reads the data
    stampa_studenti(studenti)  # Then displays it


def aggiungi_studente(percorso_file: str):
    """
    Aggiunge un nuovo studente richiedendo i dati via input e salvandoli nel file.
    
    Args:
        percorso_file: Percorso completo del file dati
        
    Note:
        - La funzione implementa la validazione dei dati in input:
          * I campi matricola, nome e cognome sono obbligatori
          * I voti devono essere numeri interi compresi tra 18 e 30
        - Utilizza cicli while per richiedere ripetutamente i dati fino a quando
          non vengono forniti in modo corretto
        - Ogni studente è rappresentato come un dizionario con chiavi standardizzate
    """
    # FASE 1: Raccolta dati con validazione
    # ----------------------------------------
    
    # Richiesta matricola obbligatoria
    while True:
        matricola = input("Matricola: ").strip()  # .strip() rimuove spazi iniziali e finali
        if matricola:
            break  # Esce dal ciclo se la matricola non è vuota
        print("⚠️ La matricola non può essere vuota. Riprova.")    # Richiesta nome obbligatorio
    while True:
        nome = input("Nome: ").strip()
        if nome:
            break
        print("⚠️ Il nome non può essere vuoto. Riprova.")

    # Richiesta cognome obbligatorio
    while True:
        cognome = input("Cognome: ").strip()
        if cognome:
            break
        print("⚠️ Il cognome non può essere vuoto. Riprova.")

    # Richiesta e validazione dei voti
    while True:
        voti_input = input("Inserisci i voti separati da virgola (es. 24,26,30): ").strip()
        try:
            # List comprehension con validazione dei voti
            voti = [
                int(v.strip()) 
                for v in voti_input.split(",") 
                if v.strip() and v.strip().isdigit()
            ]
            
            # Filtra solo i voti validi (18-30)
            voti_validi = [v for v in voti if VOTO_MIN <= v <= VOTO_MAX]
            
            if not voti_validi:
                print(f"⚠️ Inserire almeno un voto valido (tra {VOTO_MIN} e {VOTO_MAX})")
                continue
            
            voti = voti_validi  # Aggiorna la lista dei voti con solo quelli validi
            break
            
        except ValueError:
            print("⚠️ Formato non valido. Usa numeri separati da virgole.")
            continue

    # FASE 2: Creazione e salvataggio dati
    nuovo_studente = {
        "matricola": matricola,
        "nome": nome,
        "cognome": cognome,
        "voti": voti
    }

    # Load current students and add the new one
    studenti = leggi_studenti_da_file(percorso_file)
    studenti.append(nuovo_studente)  # Adds the new student to the existing list

    # Save the updated file
    with open(percorso_file, "w", encoding="utf-8") as file:
        # ensure_ascii=False allows saving non-ASCII characters (e.g. accented letters)
        # indent=2 formats JSON with 2-space indentation for better readability
        json.dump(studenti, file, ensure_ascii=False, indent=2)

    # Confirmation to user
    print(f"\n✅ Student {nome} {cognome} successfully added.")

def stampa_lista_voti_studente(percorso_file: str):
    """
    Stampa la lista dei voti per uno studente specifico identificato dalla matricola.

    Args:
        percorso_file: Percorso completo del file dati

    Note:
        - Chiede la matricola all'utente
        - Se la matricola non esiste, mostra un messaggio di errore
        - Se esiste, mostra i voti dello studente
    """
    studenti = leggi_studenti_da_file(percorso_file)
    matricola_input = input("Inserisci il numero di matricola dello studente: ").strip()
    studente = next((s for s in studenti if s.get("matricola") == matricola_input), None)
    if not studente:
        print(f"❌ Errore: Nessuno studente trovato con matricola {matricola_input}")
        return
    voti = studente.get("voti", [])
    if not voti:
        print("⚠️ Nessun voto disponibile per questo studente.")
    else:
        print("I voti sono:")
        for voto in voti:
            print(f"- {voto}")

def aggiungi_voto(percorso_file: str):
    """
    Aggiunge un voto a uno studente esistente identificato per matricola.
    
    Args:
        percorso_file: Percorso completo del file dati
        
    Note:
        - Cerca lo studente tramite la matricola usando la funzione next() con un generatore
        - Valida il voto inserito assicurandosi che sia un intero tra 18 e 30
        - Usa il metodo setdefault() per gestire il caso in cui lo studente non abbia già voti
    """
    # Carica i dati attuali
    studenti = leggi_studenti_da_file(percorso_file)

    # Richiesta della matricola
    matricola_input = input("Inserisci il numero di matricola: ").strip()

    # Ricerca dello studente con la matricola inserita
    # La funzione next() prende:
    # - Un generatore (espressione che produce valori uno alla volta)
    # - Un valore di default (None) da restituire se il generatore è vuoto
    studente_trovato = next((s for s in studenti if s.get("matricola") == matricola_input), None)

    # Verifica se lo studente è stato trovato
    if not studente_trovato:
        print(f"❌ Errore: Nessuno studente trovato con matricola {matricola_input}")
        return  # Esce dalla funzione    # Richiesta e validazione del nuovo voto
    voto_input = input("Inserisci il nuovo voto: ").strip()
    try:
        voto = int(voto_input)  # Converte l'input in numero intero
        if not 18 <= voto <= 30:  # Verifica il range consentito
            raise ValueError  # Genera un'eccezione se il voto non è nel range
    except ValueError:
        print("❌ Errore: Il voto deve essere un numero intero tra 18 e 30.")
        return  # Esce dalla funzione

    # Aggiunta del voto all'elenco
    # setdefault() restituisce il valore della chiave se esiste o crea la chiave
    # con il valore di default specificato (lista vuota in questo caso)
    studente_trovato.setdefault("voti", []).append(voto)

    # Salvataggio nel file
    with open(percorso_file, "w", encoding="utf-8") as file:
        json.dump(studenti, file, ensure_ascii=False, indent=2)

    # Conferma all'utente
    print(f"✅ Voto {voto} aggiunto con successo a {studente_trovato['nome']} {studente_trovato['cognome']}.")


def cancella_studente(percorso_file: str):
    """
    Cancella uno studente esistente dal registro identificandolo per matricola.
    
    Args:
        percorso_file: Percorso completo del file dati
        
    Note:
        - Cerca lo studente tramite la matricola
        - Richiede conferma prima di procedere con la cancellazione
        - Aggiorna il file JSON dopo la cancellazione
    """
    # Carica i dati attuali
    studenti = leggi_studenti_da_file(percorso_file)
    
    # Se non ci sono studenti nel registro
    if not studenti:
        print("❌ Nessuno studente presente nel registro.")
        return
    
    # Richiesta della matricola
    matricola_input = input("Inserisci il numero di matricola dello studente da cancellare: ").strip()
    
    # Ricerca dello studente con la matricola inserita
    studente_index = None
    for index, studente in enumerate(studenti):
        if studente.get("matricola") == matricola_input:
            studente_index = index
            break
    
    # Verifica se lo studente è stato trovato
    if studente_index is None:
        print(f"❌ Errore: Nessuno studente trovato con matricola {matricola_input}")
        return
    
    # Ottieni i dati dello studente per la conferma
    studente = studenti[studente_index]
    nome_completo = f"{studente.get('nome', 'N/D')} {studente.get('cognome', 'N/D')}"
    
    # Chiedi conferma prima di procedere
    conferma = input(f"Sei sicuro di voler cancellare lo studente {nome_completo}? (s/n): ").strip().lower()
    if conferma != 's':
        print("Operazione annullata.")
        return
    
    # Rimuovi lo studente dalla lista
    studente_rimosso = studenti.pop(studente_index)

    # Salvataggio nel file
    with open(percorso_file, "w", encoding="utf-8") as file:
        json.dump(studenti, file, ensure_ascii=False, indent=2)

    # Conferma all'utente
    print(f"✅ Studente {nome_completo} rimosso con successo dal registro.")

# Menu principale del programma
def menu():
    azioni = {
        "1": ("Visualizza lista studenti", stampa_studenti),
        "2": ("Aggiungi studente", aggiungi_studente),
        "3": ("Aggiungi voto", aggiungi_voto),
        "4": ("Cancella studente", cancella_studente),
    }
    
    while True:
        print(f"\n{Fore.CYAN}=== Registro Studenti ==={Fore.RESET}")
        for k, (desc, _) in azioni.items():
            print(f"[{k}] {desc}")
        print("[0] Esci")
        
        scelta = input("\nScelta: ").strip()
        if scelta == "0":
            print(f"{Fore.YELLOW}👋 Arrivederci!{Fore.RESET}")
            break
        elif scelta in azioni:
            azioni[scelta][1](file_path)
        else:
            print(f"{Fore.RED}❌ Scelta non valida.{Fore.RESET}")

if __name__ == "__main__":
    menu()
