import ttkbootstrap as tk
from PIL import Image, ImageTk, ImageDraw
import tkinter.filedialog as fd
from tkinter import messagebox
import json
import os
import contacts_manager as cm
from tkinter import font

# Créer la fenêtre principale
root = tk.Window(
    title="Sample App",
    themename="cosmo",
    size=(600, 600)
)

# Modify default font globally
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=12)

def afficher_contact(nom, chemin_image, phone):
    '''Graphic display of contacts.'''
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

    tk.Label(item_frame, text="Téléphone: " + phone).pack(side="left", pady=(10, 0))
    # label_name = tk.Label(item_frame, text=phone)
    # label_name.pack(side="left")

     # Delete button
    def delete_contact():
        if messagebox.askyesno("Confirmer la suppression", f"Supprimer le contact {nom}?"):
            cm.delete_contact_from_file(nom)  # Remove from JSON
            item_frame.destroy()  # Remove the contact's frame from the UI

    delete_btn = tk.Button(item_frame, text="Delete", command=delete_contact,style="Danger.TButton")
    delete_btn.pack(side="left", padx=5)

# Formulaire ajout contact
def ouvrir_formulaire():
    '''Open a new window with a form to add a contact.'''

    def check_image_exists(event=None):
        """ 
        Check if the path in the image entry field points to an existing file.

        This function is triggered either when the user types in the entry field or after a file is selected via the file dialog. It updates the status label to indicate whether the file exists.
        """
        path = entry_image.get()
        if os.path.isfile(path):
            label_status.config(text="✅ Image file found", bootstyle="success")
        else:
            label_status.config(text="❌ Image file not found", bootstyle="danger")

    def parcourir_image():
        """
        Open a file dialog to allow the user to select an image file.

        If a file is selected, its path is inserted into the entry field, and a check is performed to verify whether the file exists.
        """
        filepath = fd.askopenfilename(
            title="Choisir une image",
            filetypes=[("Images", "*.jpg *.png *.jpeg *.gif")]
        )
        if filepath:
            entry_image.delete(0, "end")
            entry_image.insert(0, filepath)
            check_image_exists()  # Call the check after selecting a file

    form = tk.Toplevel(root)
    form.title("Ajouter un contact")
    # form.geometry("400x800")
    form.resizable(False, False)

    # Add a container frame
    content = tk.Frame(form, padding=20)
    content.pack(fill="both", expand=True)

    tk.Label(content, text="Nom :").pack(pady=(10, 0))
    entry_nom = tk.Entry(content)
    entry_nom.pack()

    tk.Label(content, text="Téléphone :").pack(pady=(10, 0))
    entry_phone = tk.Entry(content)
    entry_phone.pack()

    tk.Label(content, text="Image :").pack(pady=(10, 0))
    entry_image = tk.Entry(content)
    entry_image.pack()
    # Check on each key release
    entry_image.bind("<KeyRelease>", check_image_exists)
    # Status label to show the result
    label_status = tk.Label(content, text="")
    label_status.pack(pady=(5, 0))

    browse_btn = tk.Button(content, text="Parcourir...", command=parcourir_image)
    browse_btn.pack(pady=(5, 10))

    def ajouter_contact():
        '''Process the form to add a contact and update the contacts list.'''
        nom = entry_nom.get().strip()
        image = entry_image.get().strip()
        phone = entry_phone.get().strip()

        if not nom and not image and not phone:
            messagebox.showwarning("Champs vides", "Veuillez remplir au moins un champ.")
            return

        if not image:
            image = "placeholder.jpg"

        # TODO check if the path correctly leads to an image file

        try:
            cm.ajouter_contact_moteur(nom, image, phone)
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return

        # Rafraîchir l'affichage de la liste
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        for c in cm.contacts:
            afficher_contact(c["name"], c["image"], c["phone"])

        form.destroy()

        cm.sauvegarder_contacts()

    submit_btn = tk.Button(form, text="Ajouter", bootstyle="success", command=ajouter_contact)
    submit_btn.pack(pady=10)

cm.charger_contacts()
cm.contacts.sort(key=lambda c: c["name"].lower())

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

for contact in cm.contacts:
    afficher_contact(contact["name"], contact["image"], contact["phone"])

if __name__== "__main__":
    root.place_window_center()
    root.mainloop()
