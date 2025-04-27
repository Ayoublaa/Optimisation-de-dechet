import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Fonction de calcul du coût
def calculer_cout():
    points = {
        "A": (200, 300),
        "B": (350, 150),
        "C": (200, 150)
    }

    resultat_text.delete("1.0", tk.END)

    points_faisables = {}
    for nom, (x, y) in points.items():
        if x + y >= 500:
            cout = 50 * x + 70 * y
            points_faisables[nom] = {"coord": (x, y), "cout": cout}
            resultat_text.insert(tk.END, f"{nom} : {x}, {y} -> Coût = {cout} DH\n")
        else:
            resultat_text.insert(tk.END, f"{nom} : {x}, {y} -> Non faisable (x + y < 500)\n")

    if points_faisables:
        solution = min(points_faisables.items(), key=lambda item: item[1]['cout'])
        resultat_text.insert(tk.END, "\n>>> Solution optimale :\n")
        resultat_text.insert(tk.END, f"Point {solution[0]} : {solution[1]['coord']}\n")
        resultat_text.insert(tk.END, f"Coût minimum = {solution[1]['cout']} DH")
    else:
        resultat_text.insert(tk.END, "\nAucune solution faisable trouvée.")

# Fonction d'affichage du graphique
def afficher_graphe():
    fig, ax = plt.subplots(figsize=(5, 5))

    x = np.linspace(0, 600, 400)
    y1 = np.full_like(x, 150)             # y = 150
    y2 = np.maximum(0, 500 - x)           # x + y = 500 → y = 500 - x
    x_vert = np.full_like(x, 200)         # x = 200

    ax.plot(x, y1, label='y = 150', color='blue')
    ax.plot(x, y2, label='x + y = 500', color='green')
    ax.plot(x_vert, x, label='x = 200', color='red')

    # Zone faisable (remplissage)
    x_fill = np.linspace(200, 500, 300)
    y_fill = np.maximum(150, 500 - x_fill)
    ax.fill_between(x_fill, y_fill, 600, where=y_fill<=600, color='violet', alpha=0.3, label='Zone faisable')

    # Points d'intersection
    ax.plot(200, 300, 'ko')  # A
    ax.plot(350, 150, 'ko')  # B
    ax.text(200, 300, " A", fontsize=10)
    ax.text(350, 150, " B", fontsize=10)

    ax.set_xlim(100, 550)
    ax.set_ylim(100, 400)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Zone faisable - Minimisation de coût")
    ax.legend()
    ax.grid(True)

    # Affichage dans Tkinter
    canvas = FigureCanvasTkAgg(fig, master=fenetre)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

# Interface Tkinter
fenetre = tk.Tk()
fenetre.title("Projet Final - Minimisation de Coût")
fenetre.geometry("650x750")

titre = tk.Label(fenetre, text="Minimisation de Coût - Interface Graphique", font=("Helvetica", 16, "bold"))
titre.pack(pady=10)

btn_frame = ttk.Frame(fenetre)
btn_frame.pack()

btn_calcul = ttk.Button(btn_frame, text="Calculer le coût minimum", command=calculer_cout)
btn_calcul.grid(row=0, column=0, padx=10)

btn_graphe = ttk.Button(btn_frame, text="Afficher la zone faisable", command=afficher_graphe)
btn_graphe.grid(row=0, column=1, padx=10)

resultat_text = tk.Text(fenetre, height=10, width=70, font=("Courier", 10))
resultat_text.pack(pady=10)

fenetre.mainloop()