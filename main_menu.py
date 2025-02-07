# ui/main_menu.py

import tkinter as tk
from tkinter import ttk, messagebox
from ui.inventory_gui import InventoryGUI
from inventory.manager import TugboatInventory  # Ensure this import is correct

class MainMenuGUI:
    def __init__(self, root, current_user):
        self.root = root
        self.current_user = current_user
        self.root.title("Tugboat Inventory and Ticketing System - Main Menu")
        self.root.geometry("600x500")
        self.setup_ui()

    def setup_ui(self):
        # Main container frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill="both")

        # Title Label
        title_label = ttk.Label(main_frame, text=f"Welcome, {self.current_user.username}!", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        # Frame to hold the buttons grid
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(expand=True, fill="both", pady=20)

        # List of options: (label text, callback function)
        options = [
            ("Inventory Management", self.open_inventory_management),
            ("Maintenance Ticketing", self.open_maintenance_ticketing),
            ("Safety Ticketing", self.open_safety_ticketing),
            ("Recurring Ticket Management", self.open_recurring_ticket_management),
            ("Advanced Reporting", self.open_advanced_reporting),
            ("Process Notifications", self.open_process_notifications),
            ("View Audit Logs", self.open_audit_logs),
            ("Log Out", self.logout_application)
        ]

        # Create a grid: 2 columns x 4 rows
        for idx, (text, callback) in enumerate(options):
            btn = ttk.Button(buttons_frame, text=text, command=callback, compound="top")

            row = idx // 2
            col = idx % 2
            btn.grid(row=row, column=col, padx=20, pady=20, ipadx=10, ipady=10, sticky="nsew")

        # Make the grid cells expand evenly
        for col in range(2):
            buttons_frame.columnconfigure(col, weight=1)
        for row in range(4):
            buttons_frame.rowconfigure(row, weight=1)

    # Callback functions
    def open_inventory_management(self):
        # Open a new window for the Inventory Management GUI
        inv_root = tk.Toplevel(self.root)
        inventory_manager = TugboatInventory()  # You might want to pass the existing inventory manager
        InventoryGUI(inv_root, inventory_manager)

    def open_maintenance_ticketing(self):
        messagebox.showinfo("Maintenance Ticketing", "Open Maintenance Ticketing GUI...")

    def open_safety_ticketing(self):
        messagebox.showinfo("Safety Ticketing", "Open Safety Ticketing GUI...")

    def open_recurring_ticket_management(self):
        messagebox.showinfo("Recurring Ticket Management", "Open Recurring Ticket Management GUI...")

    def open_advanced_reporting(self):
        messagebox.showinfo("Advanced Reporting", "Open Advanced Reporting GUI...")

    def open_process_notifications(self):
        messagebox.showinfo("Process Notifications", "Open Process Notifications GUI...")

    def open_audit_logs(self):
        messagebox.showinfo("View Audit Logs", "Open Audit Logs GUI...")

    def logout_application(self):
        self.root.destroy()
        run_login()

def run_main_menu(current_user):
    root = tk.Tk()
    app = MainMenuGUI(root, current_user)
    root.mainloop()

# For testing purposes:
if __name__ == '__main__':
    class DummyUser:
        username = "Test User"
    run_main_menu(DummyUser())
