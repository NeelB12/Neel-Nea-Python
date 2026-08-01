import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "users.json"

if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w") as f:
        json.dump({}, f)


def load_users():
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_users(users):
    with open(FILE_NAME, "w") as f:
        json.dump(users, f, indent=4)


def register_window():
    window = tk.Toplevel(root)
    window.title("Register")
    window.geometry("300x180")
    window.resizable(False, False)

    tk.Label(window, text="Username").pack(pady=5)
    username = tk.Entry(window)
    username.pack()

    tk.Label(window, text="Password").pack(pady=5)
    password = tk.Entry(window, show="*")
    password.pack()

    def register():
        users = load_users()

        user = username.get().strip()
        pwd = password.get().strip()

        if user == "" or pwd == "":
            messagebox.showerror("Error", "Fill in all fields.")
            return

        if user in users:
            messagebox.showerror("Error", "Username already exists.")
            return

        users[user] = pwd
        save_users(users)

        messagebox.showinfo("Success", "Registration Successful!")
        window.destroy()

    tk.Button(window, text="Register", command=register).pack(pady=15)


def login_window():
    window = tk.Toplevel(root)
    window.title("Login")
    window.geometry("300x180")
    window.resizable(False, False)

    tk.Label(window, text="Username").pack(pady=5)
    username = tk.Entry(window)
    username.pack()

    tk.Label(window, text="Password").pack(pady=5)
    password = tk.Entry(window, show="*")
    password.pack()

    def login():
        users = load_users()

        user = username.get().strip()
        pwd = password.get().strip()

        if user in users and users[user] == pwd:
            messagebox.showinfo("Success", "Login Successful!")
            root.destroy()      # Closes the whole application
        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password.\nPlease try again."
            )

    tk.Button(window, text="Login", command=login).pack(pady=15)


root = tk.Tk()
root.title("Driving Simulator")
root.geometry("300x220")
root.resizable(False, False)

tk.Label(
    root,
    text="Driving Simulator",
    font=("Arial", 16, "bold")
).pack(pady=20)

tk.Button(root, text="Register", width=20, command=register_window).pack(pady=5)
tk.Button(root, text="Login", width=20, command=login_window).pack(pady=5)
tk.Button(root, text="Exit", width=20, command=root.destroy).pack(pady=20)

root.mainloop()