from typing import List

def calcola_media(voti: List[float]) -> float:
    """
    Calcola la media aritmetica di una lista di voti numerici.
    
    Args:
        voti: Lista di voti da cui calcolare la media
        
    Returns:
        float: Media calcolata con precisione decimale, 0.0 se non ci sono voti validi
        
    Note:
        - Filtra solo i valori numerici (interi o decimali) dalla lista
        - Utilizza list comprehension per creare una nuova lista filtrata
        - Controlla che la lista non sia vuota prima di calcolare la media
    """
    voti_validi = [v for v in voti if isinstance(v, (int, float))]  # Filters only valid numbers
    return sum(voti_validi) / len(voti_validi) if voti_validi else 0.0  # Avoids division by zero