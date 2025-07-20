import tkinter as tk
from tkinter import ttk
from etudiants import open_etudiants_window
from filieres import open_filieres_window

def main():
    root = tk.Tk()
    root.title("Gestion Scolarité")
    root.geometry("500x300")

    root.configure(bg="#D4EBF8")

    menu_bar = tk.Menu(root, bg="#D4EBF8", fg="#0A3981")

    manage_menu = tk.Menu(menu_bar, tearoff=0, bg="#D4EBF8", fg="#0A3981")
    manage_menu.add_command(label="Gérer Étudiants", command=open_etudiants_window)
    manage_menu.add_command(label="Gérer Filières", command=open_filieres_window)
    menu_bar.add_cascade(label="Gestion", menu=manage_menu)

    root.config(menu=menu_bar)

    label = tk.Label(root, text="Bienvenue dans le système de gestion de scolarité!", font=("Helvetica", 16, "bold"), bg="#D4EBF8", fg="#E38E49")
    label.pack(pady=20)

    button_style = ttk.Style()
    button_style.configure("TButton", font=("Arial", 12), padding=10, relief="flat", background="#4682B4", foreground="#1F509A")

    ttk.Button(root, text="Gérer Étudiants", command=open_etudiants_window, style="TButton").pack(pady=10, fill="x", padx=50)
    ttk.Button(root, text="Gérer Filières", command=open_filieres_window, style="TButton").pack(pady=10, fill="x", padx=50)

    root.mainloop()

if __name__ == "__main__":
    main()
