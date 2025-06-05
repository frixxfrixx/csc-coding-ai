from typing import List, Dict, Tuple
from src.models.studente import Studente
from src.utils.input_validator import InputValidator
from src.utils.file_handler import FileHandler

class DatabaseUpdater:
    def __init__(self, file_handler: FileHandler, validator: InputValidator):
        self.file_handler = file_handler
        self.validator = validator

    def trova_matricole_non_valide(self) -> List[Studente]:
        """Trova tutti gli studenti con matricole non valide"""
        studenti = self.file_handler.load_students()
        return [s for s in studenti if not self.validator.valida_matricola(s.matricola)]

    def aggiorna_matricole(self, modalita_interattiva: bool = True) -> Tuple[int, List[Dict]]:
        """
        Controlla e aggiorna le matricole non valide nel database.
        
        Args:
            modalita_interattiva: Se True, chiede conferma per ogni aggiornamento
            
        Returns:
            Tuple[int, List[Dict]]: Numero di matricole aggiornate e lista dei cambiamenti
        """
        studenti = self.file_handler.load_students()
        matricole_aggiornate = []
        contatore_aggiornamenti = 0

        for studente in studenti:
            if not self.validator.valida_matricola(studente.matricola):
                vecchia_matricola = studente.matricola
                print(f"\nStudente trovato con matricola non valida:")
                print(f"Nome: {studente.nome} {studente.cognome}")
                print(f"Matricola attuale: {vecchia_matricola}")
                
                if modalita_interattiva:
                    while True:
                        nuova_matricola = input("Inserisci la nuova matricola (5-10 cifre): ").strip()
                        if self.validator.valida_matricola(nuova_matricola):
                            break
                        print("❌ Matricola non valida! Deve contenere tra 5 e 10 cifre.")
                else:
                    # Genera automaticamente una nuova matricola
                    nuova_matricola = self._genera_nuova_matricola(vecchia_matricola)

                # Aggiorna la matricola
                studente.matricola = nuova_matricola
                matricole_aggiornate.append({
                    'nome': studente.nome,
                    'cognome': studente.cognome,
                    'vecchia': vecchia_matricola,
                    'nuova': nuova_matricola
                })
                contatore_aggiornamenti += 1

        # Salva le modifiche se ci sono stati aggiornamenti
        if contatore_aggiornamenti > 0:
            if self.file_handler.save_students(studenti):
                print("\n✅ Database aggiornato con successo!")
            else:
                print("\n❌ Errore durante il salvataggio delle modifiche!")

        return contatore_aggiornamenti, matricole_aggiornate

    def _genera_nuova_matricola(self, vecchia_matricola: str) -> str:
        """Genera una nuova matricola valida basata sulla vecchia"""
        # Se la matricola è numerica, aggiunge zeri all'inizio
        if vecchia_matricola.isdigit():
            return vecchia_matricola.zfill(5)
        # Altrimenti genera una nuova matricola casuale
        import random
        return str(random.randint(10000, 99999))