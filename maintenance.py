# tickets/maintenance.py

class MaintenanceTicket:
    def __init__(self, description, required_items):
        """
        Initialize a maintenance ticket.

        :param description: Description of the maintenance task.
        :param required_items: Dictionary of required items in the format
                               {item_number: quantity, ...}.
        """
        self.description = description
        self.required_items = required_items  # e.g., {"A123": 2, "B456": 1}
        self.comments = []
        self.completed = False

    def add_comment(self, comment):
        """Add a comment or note to the ticket."""
        self.comments.append(comment)

    def complete_ticket(self, inventory_manager, tugboat_name):
        """
        Mark the ticket as completed and deduct the required inventory items.

        :param inventory_manager: An instance of your TugboatInventory class.
        :param tugboat_name: The name of the tugboat where the maintenance is performed.
        """
        # Loop through each required item and remove it from the inventory.
        for item_number, quantity in self.required_items.items():
            inventory_manager.remove_item(tugboat_name, item_number, quantity)

        self.completed = True
        print(f"Maintenance ticket '{self.description}' has been completed for tugboat '{tugboat_name}'.")

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return (f"Maintenance Ticket: {self.description}\n"
                f"Required Items: {self.required_items}\n"
                f"Comments: {self.comments}\n"
                f"Status: {status}")
