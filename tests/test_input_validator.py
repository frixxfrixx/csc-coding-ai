import unittest
import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.input_validator import InputValidator

class TestInputValidator(unittest.TestCase):
    def setUp(self):
        self.validator = InputValidator()

    def test_validazione_matricola(self):
        # Test casi validi (5-10 cifre)
        self.assertTrue(self.validator.valida_matricola("12345"))  # 5 cifre
        self.assertTrue(self.validator.valida_matricola("123456"))  # 6 cifre
        self.assertTrue(self.validator.valida_matricola("1234567890"))  # 10 cifre

        # Test casi non validi
        self.assertFalse(self.validator.valida_matricola("1234"))  # troppo corto
        self.assertFalse(self.validator.valida_matricola("12345678901"))  # troppo lungo
        self.assertFalse(self.validator.valida_matricola(""))  # vuoto
        self.assertFalse(self.validator.valida_matricola("abcde"))  # non numerico
        self.assertFalse(self.validator.valida_matricola("123ab"))  # alfanumerico
        self.assertFalse(self.validator.valida_matricola("12 345"))  # con spazi
        self.assertFalse(self.validator.valida_matricola("12.345"))  # con punti

if __name__ == '__main__':
    unittest.main()