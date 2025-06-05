import unittest
import os
import sys
import json

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.input_validator import InputValidator
from src.utils.file_handler import FileHandler

class TestDatabaseIntegrity(unittest.TestCase):
    def setUp(self):
        self.validator = InputValidator()
        self.file_handler = FileHandler("registro.txt")

    def test_matricole_database(self):
        """Verifica che tutte le matricole nel database siano valide"""
        studenti = self.file_handler.load_students()
        matricole_non_valide = []

        for studente in studenti:
            matricola = studente.matricola
            if not self.validator.valida_matricola(matricola):
                matricole_non_valide.append({
                    'matricola': matricola,
                    'nome': studente.nome,
                    'cognome': studente.cognome
                })

        # Se ci sono matricole non valide, stampa i dettagli e fallisci il test
        if matricole_non_valide:
            error_msg = "\nTrovate matricole non valide:\n"
            for s in matricole_non_valide:
                error_msg += f"- Matricola: {s['matricola']}, Studente: {s['nome']} {s['cognome']}\n"
            self.fail(error_msg)

if __name__ == '__main__':
    unittest.main(verbosity=2)