import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

# Import the inventory manager (your business logic)
from inventory.manager import TugboatInventory


class TugboatInventoryGUI:
    def __init__(self, root, inventory_manager):
        self.root = root
        self.inventory_manager = inventory_manager
        self.root.title("Tugboat Inventory and Ticketing System - GUI")
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Inventory Menu
        inventory_menu = tk.Menu(menubar, tearoff=0)
        inventory_menu.add_command(label="List Inventory", command=self.show_inventory)
        inventory_menu.add_command(label="Add Inventory Item", command=self.add_inventory_item)
        menubar.add_cascade(label="Inventory", menu=inventory_menu)

        # Tickets Menu
        ticket_menu = tk.Menu(menubar, tearoff=0)
        ticket_menu.add_command(label="Maintenance Tickets", command=self.show_maintenance_tickets)
        ticket_menu.add_command(label="Safety Tickets", command=self.show_safety_tickets)
        menubar.add_cascade(label="Tickets", menu=ticket_menu)

        # Reports Menu
        report_menu = tk.Menu(menubar, tearoff=0)
        report_menu.add_command(label="Inventory Report", command=self.show_inventory_report)
        report_menu.add_command(label="Usage Report", command=self.show_usage_report)
        menubar.add_cascade(label="Reports", menu=report_menu)

        # Notifications
        menubar.add_command(label="Notifications", command=self.show_notifications)

        # Audit Logs
        menubar.add_command(label="Audit Logs", command=self.show_audit_logs)

        # Exit
        menubar.add_command(label="Exit", command=self.root.quit)

    def create_widgets(self):
        # Create a main frame for the central content
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.label = ttk.Label(self.main_frame, text="Welcome to the Tugboat Inventory and Ticketing System!")
        self.label.pack()

    def show_inventory(self):
        # Ask for a tugboat name and display its inventory in a new window.
        tugboat = simpledialog.askstring("Input", "Enter Tugboat Name:", parent=self.root)
        if not tugboat:
            return
        items = self.inventory_manager.get_inventory(tugboat)
        inv_window = tk.Toplevel(self.root)
        inv_window.title(f"Inventory for {tugboat}")
        text = tk.Text(inv_window, width=80, height=20)
        text.pack()
        if not items:
            text.insert(tk.END, f"No items found for tugboat '{tugboat}'.")
        else:
            for item in items.values():
                text.insert(tk.END, str(item) + "\n\n")

    def add_inventory_item(self):
        # Open a new window to gather inventory item details.
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Inventory Item")
        fields = ["Tugboat Name", "Item Number", "Name", "Description", "Location",
                  "Unit", "Vendor", "Min Stock", "Safety Stock", "Cost", "Quantity"]
        entries = {}
        for idx, field in enumerate(fields):
            label = ttk.Label(add_window, text=field)
            label.grid(row=idx, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(add_window)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entries[field] = entry

        def submit():
            try:
                tugboat = entries["Tugboat Name"].get()
                item_number = entries["Item Number"].get()
                name = entries["Name"].get()
                description = entries["Description"].get()
                location = entries["Location"].get()
                unit = entries["Unit"].get()
                vendor = entries["Vendor"].get()
                min_stock = int(entries["Min Stock"].get())
                safety_stock = int(entries["Safety Stock"].get())
                cost = float(entries["Cost"].get())
                quantity = int(entries["Quantity"].get())
            except Exception as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
                return
            # Here we call the inventory manager to add the item.
            self.inventory_manager.add_item(
                tugboat, item_number, name, description, location, unit, vendor,
                min_stock, safety_stock, expiry_date=None, image_path=None,
                documents=None, category="General", cost=cost, quantity=quantity
            )
            messagebox.showinfo("Success", f"Added item '{name}' to tugboat '{tugboat}'.")
            add_window.destroy()

        submit_btn = ttk.Button(add_window, text="Submit", command=submit)
        submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

    def show_maintenance_tickets(self):
        # Placeholder for maintenance ticket functionality.
        messagebox.showinfo("Maintenance Tickets", "This functionality will display maintenance tickets.")

    def show_safety_tickets(self):
        # Placeholder for safety ticket functionality.
        messagebox.showinfo("Safety Tickets", "This functionality will display safety tickets.")

    def show_inventory_report(self):
        # Placeholder for inventory report functionality.
        messagebox.showinfo("Inventory Report", "This functionality will generate and display an inventory report.")

    def show_usage_report(self):
        # Placeholder for usage report functionality.
        messagebox.showinfo("Usage Report", "This functionality will generate and display a usage report.")

    def show_notifications(self):
        # Placeholder for notifications.
        messagebox.showinfo("Notifications", "This functionality will show active notifications.")

    def show_audit_logs(self):
        # Placeholder for audit logs.
        messagebox.showinfo("Audit Logs", "This functionality will display audit logs.")


def run_gui():
    root = tk.Tk()
    # Create an instance of your inventory manager. In a full integration,
    # you might load data from your storage module.
    inventory_manager = TugboatInventory()
    # For demonstration, add a couple of sample tugboats.
    sample_tugboats = ["Captain D", "Beaufort"]
    for tug in sample_tugboats:
        inventory_manager.add_tugboat(tug)
    app = TugboatInventoryGUI(root, inventory_manager)
    root.mainloop()


if __name__ == '__main__':
    run_gui()
