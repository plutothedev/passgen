import tkinter as tk
from tkinter import messagebox, filedialog
import random
import string
import json

def calculate_strength(password):
    score = 0
    length = len(password)

    if length >= 8:
        score += 1
    if any(char.islower() for char in password):
        score += 1
    if any(char.isupper() for char in password):
        score += 1
    if any(char.isdigit() for char in password):
        score += 1
    if any(char in string.punctuation for char in password):
        score += 1

    return score

def strength_description(score):
    if score == 5:
        return "Very Strong"
    elif score == 4:
        return "Strong"
    elif score == 3:
        return "Moderate"
    elif score == 2:
        return "Weak"
    else:
        return "Very Weak"

def generate_password(min_length, max_length, use_uppercase, use_lowercase, use_digits, use_special_chars, enforce_requirements):
    characters = ''
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation

    if not characters:
        messagebox.showerror("Input Error", "At least one character type must be selected.")
        return "", "Very Weak"

    length = random.randint(min_length, max_length)
    password = ''.join(random.choice(characters) for i in range(length))

    if enforce_requirements:
        while not (any(char.isupper() for char in password) and
                   any(char.isdigit() for char in password) and
                   any(char in string.punctuation for char in password)):
            password = ''.join(random.choice(characters) for i in range(length))

    strength = calculate_strength(password)
    strength_level = strength_description(strength)

    return password, strength_level

def on_generate():
    try:
        min_length = min_length_slider.get()
        max_length = max_length_slider.get()
        if min_length > max_length:
            messagebox.showerror("Input Error", "Minimum length cannot be greater than maximum length.")
            return
        
        use_uppercase = uppercase_var.get()
        use_lowercase = lowercase_var.get()
        use_digits = digits_var.get()
        use_special_chars = special_chars_var.get()
        enforce_requirements = enforce_requirements_var.get()
        
        global generated_password
        generated_password, strength_level = generate_password(min_length, max_length, use_uppercase, use_lowercase, use_digits, use_special_chars, enforce_requirements)
        if show_password_var.get():
            password_entry.config(show="")  # Show password
        else:
            password_entry.config(show="*")  # Hide password
        
        result_label.config(text=f"Generated password:")
        password_entry.delete(0, tk.END)
        password_entry.insert(0, generated_password)
        strength_label.config(text=f"Password strength: {strength_level}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for length.")

def copy_to_clipboard():
    if generated_password:
        root.clipboard_clear()
        root.clipboard_append(generated_password)
        root.update()  # Keep the clipboard contents
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def save_password():
    if not generated_password:
        messagebox.showerror("No Password", "No password to save.")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                           filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        note = note_entry.get()
        data = {"password": generated_password, "note": note}
        with open(file_path, "w") as file:
            json.dump(data, file)
        messagebox.showinfo("Saved", "Password saved successfully!")

def toggle_password_visibility():
    if show_password_var.get():
        password_entry.config(show="")  # Show password
    else:
        password_entry.config(show="*")  # Hide password

def update_language():
    lang = language_var.get()
    texts = {
        "en": {
            "title": "Password Generator",
            "min_length": "Minimum Length:",
            "max_length": "Maximum Length:",
            "include_uppercase": "Include uppercase letters (ABC)",
            "include_lowercase": "Include lowercase letters (abc)",
            "include_digits": "Include digits (123)",
            "include_special_chars": "Include special characters (!#$)",
            "show_password": "Show Password",
            "generate": "Generate Password",
            "copy": "Copy to Clipboard",
            "save": "Save Password",
            "note": "Note:",
            "strength": "Password strength:"
        },
        "es": {
            "title": "Generador de Contraseñas",
            "min_length": "Longitud Mínima:",
            "max_length": "Longitud Máxima:",
            "include_uppercase": "Incluir letras mayúsculas (ABC)",
            "include_lowercase": "Incluir letras minúsculas (abc)",
            "include_digits": "Incluir dígitos (123)",
            "include_special_chars": "Incluir caracteres especiales (!#$)",
            "show_password": "Mostrar Contraseña",
            "generate": "Generar Contraseña",
            "copy": "Copiar al Portapapeles",
            "save": "Guardar Contraseña",
            "note": "Nota:",
            "strength": "Fuerza de la contraseña:"
        },
        "fr": {
            "title": "Générateur de Mot de Passe",
            "min_length": "Longueur Minimale:",
            "max_length": "Longueur Maximale:",
            "include_uppercase": "Inclure les lettres majuscules (ABC)",
            "include_lowercase": "Inclure les lettres minuscules (abc)",
            "include_digits": "Inclure les chiffres (123)",
            "include_special_chars": "Inclure les caractères spéciaux (!#$)",
            "show_password": "Afficher le Mot de Passe",
            "generate": "Générer le Mot de Passe",
            "copy": "Copier dans le Presse-papiers",
            "save": "Enregistrer le Mot de Passe",
            "note": "Note:",
            "strength": "Force du mot de passe:"
        },
        "de": {
            "title": "Passwortgenerator",
            "min_length": "Minimale Länge:",
            "max_length": "Maximale Länge:",
            "include_uppercase": "Großbuchstaben einbeziehen (ABC)",
            "include_lowercase": "Kleinbuchstaben einbeziehen (abc)",
            "include_digits": "Ziffern einbeziehen (123)",
            "include_special_chars": "Sonderzeichen einbeziehen (!#$)",
            "show_password": "Passwort anzeigen",
            "generate": "Passwort generieren",
            "copy": "In die Zwischenablage kopieren",
            "save": "Passwort speichern",
            "note": "Notiz:",
            "strength": "Passwortstärke:"
        }
    }
    selected_texts = texts.get(lang, texts["en"])
    title_label.config(text=selected_texts["title"])
    min_length_label.config(text=selected_texts["min_length"])
    max_length_label.config(text=selected_texts["max_length"])
    uppercase_checkbox.config(text=selected_texts["include_uppercase"])
    lowercase_checkbox.config(text=selected_texts["include_lowercase"])
    digits_checkbox.config(text=selected_texts["include_digits"])
    special_chars_checkbox.config(text=selected_texts["include_special_chars"])
    show_password_checkbox.config(text=selected_texts["show_password"])
    generate_button.config(text=selected_texts["generate"])
    copy_button.config(text=selected_texts["copy"])
    save_button.config(text=selected_texts["save"])
    note_label.config(text=selected_texts["note"])
    strength_label.config(text=selected_texts["strength"])

# Create the main window
root = tk.Tk()
root.title("Password Generator")
root.geometry("500x500")
root.configure(bg="#f4f4f9")

# Create frames for better organization
input_frame = tk.Frame(root, bg="#f4f4f9")
input_frame.pack(pady=10)

options_frame = tk.Frame(root, bg="#f4f4f9")
options_frame.pack(pady=10)

result_frame = tk.Frame(root, bg="#f4f4f9")
result_frame.pack(pady=10)

language_frame = tk.Frame(root, bg="#f4f4f9")
language_frame.pack(pady=10)

# Title Label
title_label = tk.Label(root, text="Password Generator", font=("Helvetica", 16, "bold"), bg="#f4f4f9")
title_label.pack(pady=10)

# Length Range Widgets
min_length_label = tk.Label(input_frame, text="Minimum Length:", bg="#f4f4f9")
min_length_label.grid(row=0, column=0, padx=10, pady=5)
min_length_slider = tk.Scale(input_frame, from_=4, to_=20, orient=tk.HORIZONTAL, length=200, bg="#f4f4f9")
min_length_slider.set(8)  # Set default minimum length
min_length_slider.grid(row=0, column=1, padx=10, pady=5)

max_length_label = tk.Label(input_frame, text="Maximum Length:",

 bg="#f4f4f9")
max_length_label.grid(row=1, column=0, padx=10, pady=5)
max_length_slider = tk.Scale(input_frame, from_=4, to_=100, orient=tk.HORIZONTAL, length=200, bg="#f4f4f9")
max_length_slider.set(16)  # Set default maximum length
max_length_slider.grid(row=1, column=1, padx=10, pady=5)

# Options Widgets
uppercase_var = tk.BooleanVar()
lowercase_var = tk.BooleanVar()
digits_var = tk.BooleanVar()
special_chars_var = tk.BooleanVar()
enforce_requirements_var = tk.BooleanVar()
show_password_var = tk.BooleanVar()

uppercase_checkbox = tk.Checkbutton(options_frame, text="Include uppercase letters (ABC)", variable=uppercase_var, bg="#f4f4f9")
uppercase_checkbox.grid(row=0, column=0, padx=10, pady=5, sticky='w')
lowercase_checkbox = tk.Checkbutton(options_frame, text="Include lowercase letters (abc)", variable=lowercase_var, bg="#f4f4f9")
lowercase_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky='w')
digits_checkbox = tk.Checkbutton(options_frame, text="Include digits (123)", variable=digits_var, bg="#f4f4f9")
digits_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky='w')
special_chars_checkbox = tk.Checkbutton(options_frame, text="Include special characters (!#$)", variable=special_chars_var, bg="#f4f4f9")
special_chars_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky='w')
enforce_requirements_checkbox = tk.Checkbutton(options_frame, text="Enforce requirements", variable=enforce_requirements_var, bg="#f4f4f9")
enforce_requirements_checkbox.grid(row=4, column=0, padx=10, pady=5, sticky='w')

show_password_checkbox = tk.Checkbutton(options_frame, text="Show Password", variable=show_password_var, command=toggle_password_visibility, bg="#f4f4f9")
show_password_checkbox.grid(row=5, column=0, padx=10, pady=5, sticky='w')

# Buttons
generate_button = tk.Button(root, text="Generate Password", command=on_generate, bg="#4CAF50", fg="white")
generate_button.pack(pady=10)

copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="#2196F3", fg="white")
copy_button.pack(pady=10)

save_button = tk.Button(root, text="Save Password", command=save_password, bg="#FF5722", fg="white")
save_button.pack(pady=10)

# Result Widgets
result_label = tk.Label(result_frame, text="Generated password:", bg="#f4f4f9")
result_label.pack(pady=5)

password_entry = tk.Entry(result_frame, width=50, bg="#ffffff")
password_entry.pack(pady=5)

strength_label = tk.Label(result_frame, text="Password strength:", bg="#f4f4f9")
strength_label.pack(pady=5)

note_label = tk.Label(result_frame, text="Note:", bg="#f4f4f9")
note_label.pack(pady=5)

note_entry = tk.Entry(result_frame, width=50, bg="#ffffff")
note_entry.pack(pady=5)

# Language Options
language_var = tk.StringVar(value="en")
language_menu = tk.OptionMenu(language_frame, language_var, "en", "es", "fr", "de", command=lambda _: update_language())
language_menu.pack(pady=5)

# Initialize the UI with default language
update_language()

# Run the application
root.mainloop()