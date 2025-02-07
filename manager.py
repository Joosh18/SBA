# inventory/models.py

from datetime import datetime

class InventoryItem:
    def __init__(self,
                 item_number,
                 name,
                 description="",
                 location="",
                 unit="each",
                 vendor="",
                 min_stock=0,
                 safety_stock=0,
                 expiry_date=None,
                 image_path=None,
                 documents=None,
                 category="Uncategorized",
                 cost=0.0,
                 quantity=0):
        """
        Initialize a comprehensive inventory item.

        :param item_number: Unique identifier for the item.
        :param name: The item name.
        :param description: Detailed description/specifications.
        :param location: Storage location (e.g., "Engine Room").
        :param unit: Unit of measure (e.g., "each", "liters").
        :param vendor: Vendor or supplier information.
        :param min_stock: Minimum stock level (reorder point).
        :param safety_stock: Additional buffer stock.
        :param expiry_date: Expiry date (datetime object) if applicable.
        :param image_path: File path or URL to an image.
        :param documents: List of associated document paths/URLs.
        :param category: Category or classification.
        :param cost: Cost per unit.
        :param quantity: Initial quantity on hand.
        """
        self.item_number = item_number
        self.name = name
        self.description = description
        self.location = location
        self.unit = unit
        self.vendor = vendor
        self.min_stock = min_stock
        self.safety_stock = safety_stock
        self.expiry_date = expiry_date  # Should be a datetime or None
        self.image_path = image_path
        self.documents = documents if documents is not None else []
        self.category = category
        self.cost = cost
        self.quantity = quantity
        self.usage_history = []  # Each record: {'timestamp': datetime, 'quantity': int}
        self.maintenance_records = []  # Each record can be a dict with details about the maintenance event

    def add(self, quantity):
        """Add a non-negative quantity to the current on-hand amount."""
        if quantity < 0:
            print("Cannot add a negative quantity.")
            return
        self.quantity += quantity

    def remove(self, quantity):
        """
        Remove a non-negative quantity if available.
        Records the removal in usage history.
        """
        if quantity < 0:
            print("Cannot remove a negative quantity.")
            return

        if self.quantity >= quantity:
            self.quantity -= quantity
            self.usage_history.append({
                'timestamp': datetime.now(),
                'quantity': quantity
            })
        else:
            print(f"Not enough {self.name} in stock. Current quantity: {self.quantity}")

    def check_reorder(self):
        """
        Check if current quantity is less than or equal to the sum of the minimum stock level
        and safety stock (i.e. a reorder is needed).
        """
        return self.quantity <= (self.min_stock + self.safety_stock)

    def add_maintenance_record(self, record):
        """
        Add a maintenance record (for example, installation or inspection details).

        :param record: A dictionary with maintenance details.
        """
        self.maintenance_records.append(record)

    def get_usage_cost(self, period="monthly"):
        """
        Calculate the total cost of items removed (used) within a specified period.

        :param period: 'monthly', 'quarterly', or 'yearly'
        :return: Total cost of usage in that period.
        """
        now = datetime.now()
        if period == "monthly":
            delta = 30 * 24 * 3600  # seconds in 30 days
        elif period == "quarterly":
            delta = 90 * 24 * 3600
        elif period == "yearly":
            delta = 365 * 24 * 3600
        else:
            print("Invalid period. Use 'monthly', 'quarterly', or 'yearly'.")
            return 0.0

        total_cost = 0.0
        for record in self.usage_history:
            elapsed = (now - record['timestamp']).total_seconds()
            if elapsed <= delta:
                total_cost += record['quantity'] * self.cost
        return total_cost

    def is_expired(self):
        """Check whether the item is expired (if an expiry date is set)."""
        if self.expiry_date is None:
            return False
        return datetime.now() > self.expiry_date

    def __str__(self):
        """Return a human-readable representation of the inventory item."""
        expiry_str = self.expiry_date.strftime("%Y-%m-%d") if self.expiry_date else "N/A"
        return (f"Item Number: {self.item_number}\n"
                f"Name: {self.name}\n"
                f"Description: {self.description}\n"
                f"Location: {self.location}\n"
                f"Unit: {self.unit}\n"
                f"Vendor: {self.vendor}\n"
                f"Category: {self.category}\n"
                f"Quantity On Hand: {self.quantity} {self.unit}\n"
                f"Cost per Unit: ${self.cost:.2f}\n"
                f"Min Stock Level: {self.min_stock} and Safety Stock: {self.safety_stock}\n"
                f"Reorder Needed: {'Yes' if self.check_reorder() else 'No'}\n"
                f"Expiry Date: {expiry_str}\n"
                f"Image: {self.image_path if self.image_path else 'No image provided'}\n"
                f"Documents: {', '.join(self.documents) if self.documents else 'None'}\n"
                f"Usage Cost (Monthly): ${self.get_usage_cost('monthly'):.2f}\n"
                f"Maintenance Records: {len(self.maintenance_records)} recorded")


class TugboatInventory:
    def __init__(self):
        # Dictionary mapping tugboat names to another dictionary of inventory items
        # The inner dictionary maps unique item numbers to InventoryItem instances.
        self.inventory = {}

    def add_tugboat(self, tugboat_name):
        """Add a new tugboat to the system."""
        if tugboat_name not in self.inventory:
            self.inventory[tugboat_name] = {}
        else:
            print(f"Tugboat '{tugboat_name}' already exists.")

    def add_item(self,
                 tugboat_name,
                 item_number,
                 name,
                 description="",
                 location="",
                 unit="each",
                 vendor="",
                 min_stock=0,
                 safety_stock=0,
                 expiry_date=None,
                 image_path=None,
                 documents=None,
                 category="Uncategorized",
                 cost=0.0,
                 quantity=0):
        """
        Add a new inventory item or update an existing one for a specific tugboat.
        If the item already exists (based on item_number), the quantity is increased.
        """
        if tugboat_name not in self.inventory:
            print(f"Tugboat '{tugboat_name}' not found.")
            return

        tugboat_inventory = self.inventory[tugboat_name]
        if item_number in tugboat_inventory:
            # Update the existing item's quantity.
            tugboat_inventory[item_number].add(quantity)
        else:
            # Create and add a new InventoryItem.
            new_item = InventoryItem(item_number, name, description, location, unit, vendor,
                                       min_stock, safety_stock, expiry_date, image_path,
                                       documents, category, cost, quantity)
            tugboat_inventory[item_number] = new_item

    def remove_item(self, tugboat_name, item_number, quantity):
        """Remove a specified quantity of an item from a tugboat's inventory."""
        if tugboat_name in self.inventory and item_number in self.inventory[tugboat_name]:
            self.inventory[tugboat_name][item_number].remove(quantity)
        else:
            print("Item or tugboat not found.")

    def get_inventory(self, tugboat_name):
        """Retrieve the inventory dictionary for a given tugboat."""
        return self.inventory.get(tugboat_name, {})

    def list_all_inventories(self):
        """Return the complete inventory for all tugboats."""
        return self.inventory
