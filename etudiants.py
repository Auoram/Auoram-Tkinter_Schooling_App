import tkinter as tk
from tkinter import ttk, messagebox
import xml.etree.ElementTree as ET

def load_etudiants_data():
    try:
        tree = ET.parse("scolarite.xml")
        root = tree.getroot()
        return tree, root.find("etudiants")
    except FileNotFoundError:
        root = ET.Element("data")
        ET.SubElement(root, "etudiants")
        ET.SubElement(root, "filieres")
        tree = ET.ElementTree(root)
        tree.write("scolarite.xml")
        return tree, root.find("etudiants")

def open_etudiants_window():
    tree, etudiants = load_etudiants_data()

    window = tk.Toplevel()
    window.title("Gérer Étudiants")
    window.geometry("700x500")

    fields = ["idE", "name", "email", "classe_id"]

    def get_next_id():
        max_id = 0
        for item in etudiants:
            max_id = max(max_id, int(item.find("idE").text))
        return str(max_id + 1)

    def clear_fields():
        for entry in input_entries.values():
            entry.delete(0, tk.END)

    def refresh_treeview():
        treeview.delete(*treeview.get_children())
        for item in etudiants:
            values = [item.find(field).text for field in fields]
            treeview.insert("", "end", values=values)

    def add_etudiant():
        inputs = {field: entry.get() for field, entry in input_entries.items() if field != "idE"}
        if any(value == "" for value in inputs.values()):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires!")
            return

        new_item = ET.Element("etudiant")
        for field, value in inputs.items():
            ET.SubElement(new_item, field).text = value
        ET.SubElement(new_item, "idE").text = get_next_id()
        etudiants.append(new_item)
        tree.write("scolarite.xml")
        messagebox.showinfo("Succès", "Étudiant ajouté avec succès!")
        refresh_treeview()
        clear_fields()

    def edit_etudiant():
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Aucun étudiant sélectionné!")
            return

        selected_values = treeview.item(selected_item, "values")
        for item in etudiants:
            if item.find("idE").text == selected_values[0]:
                for field, entry in input_entries.items():
                    if field != "idE":
                        item.find(field).text = entry.get()
                tree.write("scolarite.xml")
                messagebox.showinfo("Succès", "Étudiant modifié avec succès!")
                refresh_treeview()
                clear_fields()
                return

    def delete_etudiant():
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Aucun étudiant sélectionné!")
            return

        selected_values = treeview.item(selected_item, "values")
        for item in etudiants:
            if item.find("idE").text == selected_values[0]:
                etudiants.remove(item)
                tree.write("scolarite.xml")
                messagebox.showinfo("Succès", "Étudiant supprimé avec succès!")
                refresh_treeview()
                return

    input_entries = {}
    form_frame = tk.Frame(window)
    form_frame.pack(pady=10)
    for i, field in enumerate(fields):
        if field == "idE":
            continue
        tk.Label(form_frame, text=f"{field.capitalize()}:").grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(form_frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        input_entries[field] = entry

    tk.Button(form_frame, text="Ajouter", command=add_etudiant).grid(row=len(fields), column=0, pady=10)
    tk.Button(form_frame, text="Modifier", command=edit_etudiant).grid(row=len(fields), column=1, pady=10)
    tk.Button(form_frame, text="Supprimer", command=delete_etudiant).grid(row=len(fields), column=2, pady=10)

    treeview_frame = tk.Frame(window)
    treeview_frame.pack(pady=10)
    treeview = ttk.Treeview(treeview_frame, columns=fields, show="headings")
    for col in fields:
        treeview.heading(col, text=col.capitalize())
        treeview.column(col, width=100)
    treeview.pack()

    refresh_treeview()
