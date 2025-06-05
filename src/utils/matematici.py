from typing import List

def calcola_media(voti: List[float]) -> float:
    """Calcola la media dei voti validi"""
    voti_validi = [v for v in voti if isinstance(v, (int, float))]
    return sum(voti_validi) / len(voti_validi) if voti_validi else 0.0