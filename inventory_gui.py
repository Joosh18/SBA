# ui/inventory_gui.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from inventory.manager import TugboatInventory


# If you want to eventually display image thumbnails, you can import PIL:
# from PIL import Image, ImageTk

class InventoryGUI:
    def __init__(self, root, inventory_manager):
        self.root = root
        self.inventory_manager = inventory_manager
        self.root.title("Inventory Management")

        # Top frame for tugboat selection
        top_frame = ttk.Frame(self.root, padding="10")
        top_frame.pack(fill=tk.X)

        ttk.Label(top_frame, text="Select Tugboat:").pack(side=tk.LEFT)
        self.tugboat_var = tk.StringVar()
        tugboats = list(self.inventory_manager.inventory.keys())
        self.tugboat_combo = ttk.Combobox(top_frame, textvariable=self.tugboat_var, values=tugboats, state="readonly")
        self.tugboat_combo.pack(side=tk.LEFT, padx=5)
        if tugboats:
            self.tugboat_combo.current(0)
        self.tugboat_combo.bind("<<ComboboxSelected>>", self.load_inventory)

        # Create Treeview for grid display
        columns = ("part_number", "description", "quantity", "picture")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("part_number", text="Part Number")
        self.tree.heading("description", text="Description")
        self.tree.heading("quantity", text="Quantity On Board")
        self.tree.heading("picture", text="Picture")

        # Optionally, set fixed column widths
        self.tree.column("part_number", width=100)
        self.tree.column("description", width=300)
        self.tree.column("quantity", width=120)
        self.tree.column("picture", width=200)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Bottom frame for additional actions
        bottom_frame = ttk.Frame(self.root, padding="10")
        bottom_frame.pack(fill=tk.X)

        upload_btn = ttk.Button(bottom_frame, text="Upload Picture for Selected Item", command=self.upload_picture)
        upload_btn.pack(side=tk.LEFT)

        self.load_inventory()

    def load_inventory(self, event=None):
        # Clear current rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Determine which tugboat is selected
        tugboat = self.tugboat_var.get()
        if not tugboat:
            if self.inventory_manager.inventory:
                tugboat = list(self.inventory_manager.inventory.keys())[0]
            else:
                return

        # Retrieve items from the selected tugboat
        items = self.inventory_manager.get_inventory(tugboat)
        for item in items.values():
            # For "Picture", display the file path if set, else blank.
            picture_display = item.image_path if item.image_path else ""
            self.tree.insert("", tk.END, values=(item.item_number, item.description, item.quantity, picture_display))

    def upload_picture(self):
        # Get the selected row from the treeview
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an inventory item first.")
            return

        # Assume single selection; retrieve the part number
        item_values = self.tree.item(selected[0])["values"]
        part_number = item_values[0]

        # Open a file dialog to choose an image
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("JPEG Files", "*.jpg;*.jpeg"), ("PNG Files", "*.png"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        # Update the selected inventory item's image_path
        tugboat = self.tugboat_var.get()
        items = self.inventory_manager.get_inventory(tugboat)
        if part_number in items:
            items[part_number].image_path = file_path
            messagebox.showinfo("Upload Successful", f"Picture for part {part_number} has been updated.")
            self.load_inventory()
        else:
            messagebox.showerror("Error", "Unable to find the selected inventory item.")


if __name__ == "__main__":
    root = tk.Tk()
    # For demonstration, create an instance of TugboatInventory with sample data.
    inventory_manager = TugboatInventory()
    # Add sample tugboats
    inventory_manager.add_tugboat("Captain D")
    inventory_manager.add_tugboat("Beaufort")
    # Add sample inventory items to "Captain D"
    inventory_manager.add_item("Captain D", "PN001", "Widget A", "A standard widget", "Engine Room", "each",
                               "Acme Corp", 10, 5, None, None, None, "Components", 15.50, 25)
    inventory_manager.add_item("Captain D", "PN002", "Gadget B", "A specialized gadget", "Deck", "each", "Gadget Inc",
                               5, 2, None, None, None, "Equipment", 42.00, 10)

    app = InventoryGUI(root, inventory_manager)
    root.mainloop()
