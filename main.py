import ttkbootstrap as tk
# from tkinter import tk
from PIL import Image, ImageTk, ImageDraw

# Créer la fenêtre principale
root = tk.Window(
    title="Sample App",
    themename="cosmo",
    size=(400, 600)
)

# Exemple de contacts avec image et nom
contacts = [
    {"name": "Alice", "image": "alice.jpg"},
    {"name": "Bob", "image": "bob.jpg"},
    {"name": "Charlie", "image": "charlie.jpg"},
]

# Conteneur principal
frame = tk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

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

contacts.sort(key=lambda c: c["name"].lower())

for contact in contacts:
    try:
        img = Image.open(contact["image"]).convert("RGBA")
        img = img.resize((50, 50), Image.LANCZOS)  # ou Image.BICUBIC

    except FileNotFoundError:
        img = Image.open("placeholder.jpg").convert("RGBA")
        img = img.resize((50, 50), Image.LANCZOS)
        # img = Image.new("RGB", (50, 50), color="gray")  # Image par défaut

    # Créer un masque circulaire
    mask = Image.new("L", (50, 50), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((1, 1, 49, 49), fill=255)  # Léger décalage pour éviter les bords durs

    # Appliquer le masque pour arrondir l'image
    img.putalpha(mask)

    # Convertir en PhotoImage
    photo = ImageTk.PhotoImage(img)
    image_refs.append(photo)  # Garder une référence

    item_frame = tk.Frame(scrollable_frame, padding=10)
    item_frame.pack(fill="x")

    label_img = tk.Label(item_frame, image=photo)
    label_img.pack(side="left")

    label_name = tk.Label(item_frame, text=contact["name"], font=("Helvetica", 14))
    label_name.pack(side="left", padx=10)


if __name__== "__main__":
    root.place_window_center()
    root.mainloop()
