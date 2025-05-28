import json
import os

contacts = []

def ajouter_contact_moteur(nom, image):
    if not nom and not image:
        raise ValueError("Au moins un champ doit être rempli.")
    if not nom:
        nom = "Sans nom"
    if not image:
        image = "placeholder.jpg"
    contacts.append({"name": nom, "image": image})
    contacts.sort(key=lambda c: c["name"].lower())

def sauvegarder_contacts():
    with open("contacts.txt", "w", encoding="utf-8") as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)

def charger_contacts(fichier="contacts.txt"):
    global contacts
    if os.path.exists(fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            contacts = json.load(f)
    else:
        contacts = []  # vide si fichier absent
        # contacts = [
        #     {"name": "Alice", "image": "alice.jpg"},
        #     {"name": "Bob", "image": "bob.jpg"},
        #     {"name": "Charlie", "image": "charlie.jpg"},
        # ]
