import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog
import sqlite3

# ----------------- DATABASE SETUP -----------------
conn = sqlite3.connect("contacts.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY,
        store_name TEXT,
        phone TEXT,
        email TEXT,
        address TEXT
    )
''')
conn.commit()



# ----------------- FUNCTIONS -----------------
def add_contact():
    def save():
        store_name = entry_store.get()
        phone = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get("1.0", tk.END).strip()
        if store_name and phone:
            c.execute("INSERT INTO contacts (store_name, phone, email, address) VALUES (?, ?, ?, ?)",
                      (store_name, phone, email, address))
            conn.commit()
            messagebox.showinfo("Success", "Contact added successfully!")
            add_window.destroy()
            view_contacts()
        else:
            messagebox.showerror("Error", "Store name and phone are required.")

    add_window = tk.Toplevel(root)
    add_window.title("Add Contact")
    add_window.geometry("350x200")
    add_window.configure(bg="#09094B")


    tk.Label(add_window, text="Store Name:", bg="#F0E8DD").grid(row=0, column=0, pady=3)
    entry_store = tk.Entry(add_window,bg="#F0E8DD")
    entry_store.grid(row=0, column=1)

    tk.Label(add_window, text="Phone:", bg="#F0E8DD").grid(row=1, column=0, pady=3)
    entry_phone = tk.Entry(add_window, bg="#F0E8DD")
    entry_phone.grid(row=1, column=1)

    tk.Label(add_window, text="Email:", bg="#F0E8DD").grid(row=2, column=0, pady=3)
    entry_email = tk.Entry(add_window, bg="#F0E8DD")
    entry_email.grid(row=2, column=1)

    tk.Label(add_window, text="Address:", bg="#F0E8DD").grid(row=3, column=0, pady=3)
    entry_address = tk.Text(add_window, height=4, width=30, bg="#F0E8DD")
    entry_address.grid(row=3, column=1)

    tk.Button(add_window, text="Save", command=save, bg="#F0E8DD").grid(row=4, column=0, columnspan=2, pady=10)



def view_contacts():
    contact_list.delete(0, tk.END)
    for row in c.execute("SELECT id, store_name, phone FROM contacts"):
        contact_list.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]})")

def search_contact():
    term = simpledialog.askstring("Search", "Enter name or phone:")
    contact_list.delete(0, tk.END)
    for row in c.execute("SELECT id, store_name, phone FROM contacts WHERE store_name LIKE ? OR phone LIKE ?", (f"%{term}%", f"%{term}%")):
        contact_list.insert(tk.END, f"{row[0]} - {row[1]} ({row[2]})")

def delete_contact():
    selected = contact_list.curselection()
    if selected:
        contact_id = int(contact_list.get(selected[0]).split(" - ")[0])
        c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Contact deleted successfully.")
        view_contacts()

def update_contact():
    selected = contact_list.curselection()
    if not selected:
        return messagebox.showerror("Error", "No contact selected.")

    contact_id = int(contact_list.get(selected[0]).split(" - ")[0])
    c.execute("SELECT * FROM contacts WHERE id=?", (contact_id,))
    row = c.fetchone()

    def save():
        store_name = entry_store.get()
        phone = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get("1.0", tk.END).strip()
        c.execute("UPDATE contacts SET store_name=?, phone=?, email=?, address=? WHERE id=?",
                  (store_name, phone, email, address, contact_id))
        conn.commit()
        messagebox.showinfo("Updated", "Contact updated successfully!")
        edit_window.destroy()
        view_contacts()

    edit_window = tk.Toplevel(root)
    edit_window.title("Update Contact")
    edit_window.configure(bg="#09094B")

    tk.Label(edit_window, text="Store Name:", bg="#F0E8DD").grid(row=0, column=0, pady=3)
    entry_store = tk.Entry(edit_window, bg="#F0E8DD")
    entry_store.insert(0, row[1])
    entry_store.grid(row=0, column=1)

    tk.Label(edit_window, text="Phone:", bg="#F0E8DD").grid(row=1, column=0, pady=3)
    entry_phone = tk.Entry(edit_window, bg="#F0E8DD")
    entry_phone.insert(0, row[2])
    entry_phone.grid(row=1, column=1)

    tk.Label(edit_window, text="Email:", bg="#F0E8DD").grid(row=2, column=0, pady=3)
    entry_email = tk.Entry(edit_window, bg="#F0E8DD")
    entry_email.insert(0, row[3])
    entry_email.grid(row=2, column=1)

    tk.Label(edit_window, text="Address:", bg="#F0E8DD").grid(row=3, column=0, pady=3)
    entry_address = tk.Text(edit_window, height=4, width=30, bg="#F0E8DD")
    entry_address.insert(tk.END, row[4])
    entry_address.grid(row=3, column=1)

    tk.Button(edit_window, text="Save Changes", command=save, bg="#F0E8DD").grid(row=4, column=0, columnspan=2, pady=10)

# ----------------- GUI SETUP -----------------
root = tk.Tk()
root.title("Contact Book")
root.geometry("500x400")
root.resizable(False,False)
root.configure(bg="#01012B")

contact_list = tk.Listbox(root, width=60, height=15, bg="#F0E8DD")
contact_list.pack(pady=10)

container = tk.Frame(root, bg="#01012B", width=30, height=40)
container.pack()

btn_frame1 = tk.Frame(container, bg="#01012B") 
btn_frame1.pack(side="right", padx=5)


btn_frame3 = tk.Frame(container, bg="#01012B")  
btn_frame3.pack(side="left", padx=20)

btn_add = tk.Button(btn_frame3, text="Add Contact", fg="white", bg="black", command=add_contact)
btn_add.grid(row=0, column=1, pady=40, padx=0)

btn_view = tk.Button(btn_frame1, text="View Contacts", fg="white", bg="black", command=view_contacts)
btn_view.grid(row=0, column=4, pady=40)

btn_search = tk.Button(btn_frame3, text="Search Contact", fg="white", bg="black", command=search_contact)
btn_search.grid(row=1, column=1, padx=5)

btn_update = tk.Button(btn_frame1, text="Update Contact", fg="white", bg="black",  command=update_contact)
btn_update.grid(row=1, column=4, padx=30)

btn_delete = tk.Button(btn_frame1, text="Delete Contact",fg="white", bg="black",  command=delete_contact)
btn_delete.grid(row=1, column=1) 

label= Label(btn_frame1,bg="#F0E6D8", text= "CONTACT BOOK", border=20, font=("Helvetica", 15, "bold"))
label.grid(row=0, column=1)

view_contacts()
root.mainloop()

# ----------------- END -----------------

