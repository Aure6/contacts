import json
import os

contacts = []

def ajouter_contact():
        nom = entry_nom.get().strip()
        image = entry_image.get().strip()

        if not nom and not image:
            messagebox.showwarning("Champs vides", "Veuillez remplir au moins un champ.")
            return

        # if not nom:
        #     nom = "Sans nom"
        if not image:
            image = "placeholder.jpg"

        # Ajouter à la liste et trier
        contacts.append({"name": nom, "image": image})
        contacts.sort(key=lambda c: c["name"].lower())

        # Effacer les anciens widgets dans scrollable_frame
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Réafficher tous les contacts triés
        for c in contacts:
            afficher_contact(c["name"], c["image"])

        form.destroy()

        sauvegarder_contacts()

        submit_btn = tk.Button(form, text="Ajouter", bootstyle="success", command=ajouter_contact)
        submit_btn.pack(pady=10)

def sauvegarder_contacts():
    with open("contacts.txt", "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)

def charger_contacts():
    global contacts
    if os.path.exists("contacts.txt"):
        with open("contacts.txt", "r", encoding="utf-8") as f:
            contacts = json.load(f)
    else:
        # Liste par défaut si fichier absent
        contacts = [
            {"name": "Alice", "image": "alice.jpg"},
            {"name": "Bob", "image": "bob.jpg"},
            {"name": "Charlie", "image": "charlie.jpg"},
        ]
