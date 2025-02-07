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
        """
        self.item_number = item_number
        self.name = name
        self.description = description
        self.location = location
        self.unit = unit
        self.vendor = vendor
        self.min_stock = min_stock
        self.safety_stock = safety_stock
        self.expiry_date = expiry_date  # datetime object or None
        self.image_path = image_path
        self.documents = documents if documents is not None else []
        self.category = category
        self.cost = cost
        self.quantity = quantity
        self.usage_history = []          # Records removals: [{'timestamp': datetime, 'quantity': int}, ...]
        self.maintenance_records = []    # Maintenance events, if any.
        self.alert_active = False        # Flag to indicate if an alert has been sent

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
        Determine if the item is at or below its reorder threshold.
        The threshold is defined as (min_stock + safety_stock).
        """
        return self.quantity <= (self.min_stock + self.safety_stock)

    def add_maintenance_record(self, record):
        """Add a maintenance record (e.g., installation or inspection details)."""
        self.maintenance_records.append(record)

    def get_usage_cost(self, period="monthly"):
        """
        Calculate the total cost of items removed (used) within a specified period.
        :param period: 'monthly', 'quarterly', or 'yearly'
        :return: Total cost (float)
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
        """Return True if the item is expired (if an expiry date is set)."""
        if self.expiry_date is None:
            return False
        return datetime.now() > self.expiry_date

    def __str__(self):
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
                f"Min Stock Level: {self.min_stock} | Safety Stock: {self.safety_stock}\n"
                f"Reorder Needed: {'Yes' if self.check_reorder() else 'No'}\n"
                f"Expiry Date: {expiry_str}\n"
                f"Image: {self.image_path if self.image_path else 'No image provided'}\n"
                f"Documents: {', '.join(self.documents) if self.documents else 'None'}\n"
                f"Usage Cost (Monthly): ${self.get_usage_cost('monthly'):.2f}\n"
                f"Maintenance Records: {len(self.maintenance_records)} recorded")
