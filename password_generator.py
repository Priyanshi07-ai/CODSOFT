import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    try:
        length = int(length_entry.get())
        if length < 4:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number (at least 4) for password length.")
        return

    level = complexity.get()

    if level == "Easy":
        characters = string.ascii_letters
    elif level == "Medium":
        characters = string.ascii_letters + string.digits
    else:  # Hard
        characters = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    password_var.set(password)

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")
root.resizable(False, False)
root.config(bg="#f0f4f7")

tk.Label(root, text="Secure Password Generator", font=("Helvetica", 14, "bold"), bg="#f4f6f8").pack(pady=10)

# Password Length Entry
tk.Label(root, text="Enter Password Length:", bg="#dde6ee").pack()
length_entry = tk.Entry(root, font=("Arial", 10), justify="center")
length_entry.pack(pady=5)

# Complexity selection
tk.Label(root, text="Select Password Complexity:", foreground="white", bg="#0a3857").pack(pady=(10, 0))
complexity = tk.StringVar(value="Hard")
tk.OptionMenu(root, complexity, "Easy", "Medium", "Hard").pack(pady=5)

# Generate Button
tk.Button(root, text="Generate Password", command=generate_password, bg="#0a3857", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

# Output Box
password_var = tk.StringVar()
tk.Entry(root, textvariable=password_var, font=("Arial", 12), width=30, justify="center").pack(pady=5)

root.mainloop()
