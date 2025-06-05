from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Studente:
    matricola: str
    nome: str
    cognome: str
    voti: List[int]

    def to_dict(self) -> Dict:
        return {
            "matricola": self.matricola,
            "nome": self.nome,
            "cognome": self.cognome,
            "voti": self.voti
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Studente':
        return cls(
            matricola=data.get("matricola", ""),
            nome=data.get("nome", ""),
            cognome=data.get("cognome", ""),
            voti=data.get("voti", [])
        )