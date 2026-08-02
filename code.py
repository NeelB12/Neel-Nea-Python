# A simple driving simulator project for school work
import tkinter as tk
from tkinter import messagebox
import json
import os

FILE_NAME = "users.json"

# Create the user file if it does not already exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w") as f:
        json.dump({}, f)


def load_users():
    # Load the saved user information from the file
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_users(users):
    # Save the user information back to the file
    with open(FILE_NAME, "w") as f:
        json.dump(users, f, indent=4)


def register_window():
    # Open the registration window
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
        # Check whether the new account details are valid
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


def show_start_screen():
    # Show the next screen after a successful login
    root.withdraw()

    screen = tk.Toplevel(root)
    screen.title("Start Driving Test")
    screen.geometry("400x250")
    screen.resizable(False, False)

    tk.Label(
        screen,
        text="Start Driving Test Sim",
        font=("Arial", 16, "bold")
    ).pack(pady=35)

    def play():
        # Open the simple driving game when the play button is pressed
        screen.destroy()
        show_game_screen()

    tk.Button(
        screen,
        text="▶ Play",
        width=15,
        font=("Arial", 12, "bold"),
        command=play
    ).pack(expand=True)


def show_game_screen():
    # Create a simple top-down 2D driving game
    game_window = tk.Toplevel(root)
    game_window.title("Driving Test Sim")
    game_window.geometry("700x500")
    game_window.resizable(False, False)

    canvas = tk.Canvas(game_window, width=650, height=450, bg="#2f4f4f", highlightthickness=0)
    canvas.pack(padx=10, pady=10)

    # Draw a simple road layout
    canvas.create_rectangle(90, 50, 560, 400, fill="#444444", outline="")
    canvas.create_rectangle(220, 80, 430, 370, fill="#666666", outline="")

    for y in range(90, 370, 35):
        canvas.create_line(325, y, 325, y + 20, fill="white", width=4)

    for x in range(110, 560, 35):
        canvas.create_line(x, 225, x + 20, 225, fill="white", width=4)

    car = canvas.create_rectangle(300, 210, 340, 250, fill="#1e90ff", outline="black", width=2)

    x_pos = 300
    y_pos = 210
    speed = 8
    keys = {"w": False, "a": False, "s": False, "d": False}

    def update_game():
        nonlocal x_pos, y_pos

        if keys["w"]:
            y_pos -= speed
        if keys["s"]:
            y_pos += speed
        if keys["a"]:
            x_pos -= speed
        if keys["d"]:
            x_pos += speed

        x_pos = max(90, min(560 - 40, x_pos))
        y_pos = max(50, min(400 - 40, y_pos))

        canvas.coords(car, x_pos, y_pos, x_pos + 40, y_pos + 40)
        game_window.after(20, update_game)

    def on_key_press(event):
        key = event.keysym.lower()
        if key in keys:
            keys[key] = True

    def on_key_release(event):
        key = event.keysym.lower()
        if key in keys:
            keys[key] = False

    game_window.bind("<KeyPress>", on_key_press)
    game_window.bind("<KeyRelease>", on_key_release)
    game_window.focus_set()
    update_game()


def login_window():
    # Open the login window
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
        # Check whether the username and password match
        users = load_users()

        user = username.get().strip()
        pwd = password.get().strip()

        if user in users and users[user] == pwd:
            messagebox.showinfo("Success", "Login Successful!")
            window.destroy()
            show_start_screen()
        else:
            messagebox.showerror(
                "Login Failed",
                "Incorrect username or password.\nPlease try again."
            )

    tk.Button(window, text="Login", command=login).pack(pady=15)


root = tk.Tk()
root.title("Driving Simulator (school project)")
root.geometry("300x220")
root.resizable(False, False)

# Main menu for the project
tk.Label(
    root,
    text="Driving Simulator",
    font=("Arial", 16, "bold")
).pack(pady=20)

tk.Button(root, text="Register", width=20, command=register_window).pack(pady=5)
tk.Button(root, text="Login", width=20, command=login_window).pack(pady=5)
tk.Button(root, text="Exit", width=20, command=root.destroy).pack(pady=20)

root.mainloop()