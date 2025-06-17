"""
Modelli principali del quiz: Domanda e QuizSession.

- Domanda: rappresenta una singola domanda a scelta multipla.
- QuizSession: gestisce lo stato della sessione corrente (domande, punteggio, statistiche).

Utilizzato da:
- main.py → per orchestrare il quiz
- ui.py → per mostrare domande e raccogliere risposte
- score_calculator.py → per calcolare i punteggi

:author: Tuo Nome
:created: 2025-06-12
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class Domanda:
    """
    Rappresenta una singola domanda del quiz.

    :param testo: testo della domanda
    :param opzioni: dizionario delle opzioni (es. {"A": "...", "B": "...", ...})
    :param corretta: chiave della risposta corretta (es. "C")
    """
    testo: str
    opzioni: Dict[str, str]
    corretta: str


@dataclass
class QuizSession:
    """
    Gestisce lo stato di una sessione quiz: domande, punteggio e statistiche.

    :param domande: lista delle domande da presentare
    :param timeout: secondi disponibili per ciascuna risposta
    :param punteggio: punteggio totale corrente
    :param stats: dizionario delle statistiche (corrette, errate, tempi, ecc.)
    """
    domande: List[Domanda]
    timeout: int
    punteggio: int = 0
    stats: Dict[str, any] = field(default_factory=lambda: {
        "corrette": 0,
        "errate": 0,
        "saltate": 0,
        "tempi": [],
    })

    _index: int = 0  # indice interno della domanda corrente

    def next_question(self) -> Optional[Domanda]:
        """
        Restituisce la prossima domanda, oppure None se terminate.

        :return: Domanda successiva o None
        """
        if self._index < len(self.domande):
            domanda = self.domande[self._index]
            self._index += 1
            return domanda
        return None

    def record_answer(self, domanda: Domanda, risposta: str, tempo: float) -> Tuple[int, bool, bool]:
        """
        Registra una risposta, calcola il punteggio e aggiorna le statistiche.

        :param domanda: oggetto Domanda
        :param risposta: stringa "A"–"D" o None/""
        :param tempo: tempo impiegato per rispondere
        :return: (punti ottenuti, risposta corretta?, tempo scaduto?)
        """
        from score_calculator import calculate_score
        
        # Verifica se il tempo è scaduto
        scaduto = tempo >= self.timeout

        # Se il tempo è scaduto o la risposta è None, la domanda è saltata
        if scaduto or risposta is None:
            self.stats["saltate"] += 1
            self.stats["tempi"].append(tempo)
            return 0, False, scaduto

        # Verifica se la risposta è corretta
        is_correct = risposta == domanda.corretta
        
        # Aggiorna le statistiche
        if is_correct:
            self.stats["corrette"] += 1
        else:
            self.stats["errate"] += 1
        
        self.stats["tempi"].append(tempo)
        
        # Calcola e aggiorna il punteggio
        punti = calculate_score(is_correct, tempo, self.timeout)
        self.punteggio += punti
        
        return punti, is_correct, scaduto

