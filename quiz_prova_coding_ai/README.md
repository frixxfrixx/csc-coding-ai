# Quiz a Scelta Multipla 🎯

Quiz interattivo con interfaccia grafica (Tkinter) e web (Streamlit).

## Caratteristiche ✨

### Interfacce
- **Modalità Locale**: finestra dedicata con Tkinter
- **Modalità Web**: interfaccia browser con Streamlit

### Funzionalità
- 3 livelli di difficoltà:
  - **Facile**: 5 domande, 15 secondi per risposta
  - **Media**: 10 domande, 10 secondi per risposta
  - **Difficile**: 15 domande, 5 secondi per risposta
- Timer con barra di avanzamento visuale
- Possibilità di saltare le domande con pulsante dedicato
- Punteggio in tempo reale (visualizzato in alto a sinistra)
- Pulsante di uscita in alto a destra
- Nessun feedback immediato durante il quiz
- Riepilogo finale dettagliato con:
  - Punteggio totale
  - Risposte corrette
  - Risposte errate
  - Domande saltate
  - Tempo medio di risposta

## Requisiti 📋

- Python 3.8 o superiore
- Tkinter (incluso in Python)
- Streamlit (`pip install streamlit`)

## Struttura del Progetto 📁

```
quiz_prova_coding_ai/
│
├── main.py               # Punto di ingresso dell'applicazione
├── quiz_gui.py          # Interfaccia grafica Tkinter
├── quiz_streamlit.py    # Interfaccia web Streamlit
├── models.py            # Definizione classi Domanda e QuizSession
├── config.py            # Configurazioni (difficoltà, timeout)
├── data_loader.py       # Caricamento domande da file
├── score_calculator.py  # Calcolo punteggi
├── process_answer.py    # Gestione delle risposte
├── questions.json       # Database delle domande
└── scores.csv           # Archivio punteggi
```

## Come Iniziare 🚀

1. Clona il repository o scarica i file
2. Installa le dipendenze:
   ```powershell
   pip install streamlit
   ```
3. Avvia il quiz:
   ```powershell
   python main.py
   ```
4. Scegli la modalità:
   - `1` per interfaccia locale (Tkinter)
   - `2` per interfaccia web (Streamlit)
   - `Q` per uscire

## Modalità di Gioco 🎮

1. **Avvio**:
   - Scegli la modalità (locale o web)
   - Seleziona il livello di difficoltà

2. **Durante il Quiz**:
   - Leggi la domanda al centro dello schermo
   - Osserva il timer con barra di avanzamento
   - Scegli una delle quattro opzioni o usa il pulsante per saltare
   - Il punteggio viene aggiornato automaticamente
   - Nessun feedback immediato sulle risposte

3. **Riepilogo Finale**:
   - Visualizza statistiche complete della sessione
   - Vedi quali domande sono state corrette, errate o saltate
   - Opzione per giocare ancora o uscire

## Caratteristiche Tecniche 🔧

### Sistema di Punteggio
- Risposte corrette: punti positivi
- Risposte errate: punti negativi
- Domande saltate: 0 punti
- Bonus tempo: più punti per risposte rapide

### Gestione Timer
- Barra di avanzamento visiva
- Timeout automatico
- Conteggio tempo per statistiche

### Interfaccia Utente
- Design moderno e intuitivo
- Feedback visivo immediato
- Navigazione semplificata

## Contribuire 🤝

Per contribuire al progetto:
1. Fai un fork del repository
2. Crea un branch per le tue modifiche
3. Invia una pull request

## Autori ✍️

- frixx & ai
- Data creazione: 2025-06-17

## Licenza 📄

Questo progetto è distribuito con licenza MIT.
