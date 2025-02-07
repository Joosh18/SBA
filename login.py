# ui/login.py

import tkinter as tk
from tkinter import ttk, messagebox
from users.user_manager import UserManager


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Tugboat Inventory System - Login")
        self.root.geometry("350x200")
        self.user_manager = UserManager()
        self.logged_in_user = None  # Will store the User object on successful login

        # Variables for username and password
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True, fill="both")

        # Username label and entry
        ttk.Label(frame, text="Username:").grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        self.username_entry = ttk.Entry(frame, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, pady=(0, 10), sticky=tk.EW)
        self.username_entry.focus()

        # Password label and entry (masked)
        ttk.Label(frame, text="Password:").grid(row=1, column=0, pady=(0, 10), sticky=tk.W)
        self.password_entry = ttk.Entry(frame, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=1, column=1, pady=(0, 10), sticky=tk.EW)

        # Login button
        login_btn = ttk.Button(frame, text="Login", command=self.login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=(10, 10))

        # Error message label
        self.error_label = ttk.Label(frame, text="", foreground="red")
        self.error_label.grid(row=3, column=0, columnspan=2)

        frame.columnconfigure(1, weight=1)

    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        user = self.user_manager.validate_user(username, password)
        if user is None:
            self.error_label.config(text="Invalid username or password.")
        else:
            self.logged_in_user = user
            messagebox.showinfo("Login Successful", f"Welcome, {user.username}!")
            self.root.destroy()


def run_login():
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()
    return login_app.logged_in_user
