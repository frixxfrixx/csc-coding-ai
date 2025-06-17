import tkinter as tk

root = tk.Tk()
root.title("Quiz")

# Titolo
title_label = tk.Label(root, text="Quiz", font=("Arial", 24))
title_label.grid(row=0, column=0, columnspan=2)

# Pulsante "Inizia"
start_button = tk.Button(root, text="Inizia", command=lambda: print("Quiz avviato"))
start_button.grid(row=0, column=2)

# Area di testo per visualizzare le domande
question_label = tk.Label(root, text="Domanda:", font=("Arial", 18))
question_label.grid(row=1, column=0, columnspan=2)
question_text = tk.Text(root, height=5, width=40)
question_text.grid(row=2, column=0, columnspan=2)

# Area di testo per inserire le risposte
answer_label = tk.Label(root, text="Risposta:", font=("Arial", 18))
answer_label.grid(row=3, column=0, columnspan=2)
answer_text = tk.Text(root, height=5, width=40)
answer_text.grid(row=4, column=0, columnspan=2)

# Pulsante "Invia"
submit_button = tk.Button(root, text="Invia", command=lambda: print("Risposta inviata"))
submit_button.grid(row=5, column=0)

# Pulsante "Prossima domanda"
next_button = tk.Button(root, text="Prossima domanda", command=lambda: print("Prossima domanda"))
next_button.grid(row=5, column=1)

# Area di testo per visualizzare il punteggio
score_label = tk.Label(root, text="Punteggio:", font=("Arial", 18))
score_label.grid(row=6, column=0, columnspan=2)
score_text = tk.Text(root, height=1, width=10)
score_text.grid(row=7, column=0, columnspan=2)

root.mainloop()