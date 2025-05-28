import ttkbootstrap as tk
from PIL import Image, ImageTk, ImageDraw
import tkinter.filedialog as fd
from tkinter import messagebox
import json
import os
import contacts_manager as cm

# Créer la fenêtre principale
root = tk.Window(
    title="Sample App",
    themename="cosmo",
    size=(600, 600)
)


def afficher_contact(nom, chemin_image):
    try:
        img = Image.open(chemin_image).convert("RGBA")
        img = img.resize((50, 50), Image.LANCZOS)
    except FileNotFoundError:
        img = Image.open("placeholder.jpg").convert("RGBA")
        img = img.resize((50, 50), Image.LANCZOS)

    scale = 4
    size = 50
    high_res_mask = Image.new("L", (size*scale, size*scale), 0)
    draw = ImageDraw.Draw(high_res_mask)
    draw.ellipse((0, 0, size*scale, size*scale), fill=255)
    mask = high_res_mask.resize((size, size), Image.LANCZOS)
    img.putalpha(mask)

    photo = ImageTk.PhotoImage(img)
    image_refs.append(photo)

    item_frame = tk.Frame(scrollable_frame, padding=10)
    item_frame.pack(fill="x")

    label_img = tk.Label(item_frame, image=photo)
    label_img.pack(side="left")

    label_name = tk.Label(item_frame, text=nom, font=("Helvetica", 14))
    label_name.pack(side="left", padx=10)

# Formulaire ajout contact
def ouvrir_formulaire():
    form = tk.Toplevel(root)
    form.title("Ajouter un contact")
    form.geometry("300x200")
    form.resizable(False, False)

    tk.Label(form, text="Nom :").pack(pady=(10, 0))
    entry_nom = tk.Entry(form)
    entry_nom.pack()

    tk.Label(form, text="Image :").pack(pady=(10, 0))
    entry_image = tk.Entry(form)
    entry_image.pack()

    def parcourir_image():
        filepath = fd.askopenfilename(
            title="Choisir une image",
            filetypes=[("Images", "*.jpg *.png *.jpeg *.gif")]
        )
        if filepath:
            entry_image.delete(0, "end")
            entry_image.insert(0, filepath)

    browse_btn = tk.Button(form, text="Parcourir...", command=parcourir_image)
    browse_btn.pack(pady=(5, 10))

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

charger_contacts()
contacts.sort(key=lambda c: c["name"].lower())

################
# créer l'interface
# Conteneur principal
frame = tk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

# Bouton "Add"
add_button = tk.Button(frame, text="Ajouter un contact", bootstyle="success", command=ouvrir_formulaire)
add_button.pack(pady=(0, 10))

# Créer un canvas pour pouvoir scroller la liste
canvas = tk.Canvas(frame)
scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Charger les images et les afficher
image_refs = []  # Pour éviter que les images soient supprimées par le garbage collector

for contact in contacts:
    afficher_contact(contact["name"], contact["image"])

if __name__== "__main__":
    root.place_window_center()
    root.mainloop()
