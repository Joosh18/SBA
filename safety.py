# tickets/safety.py

class SafetyTicket:
    def __init__(self, description):
        """
        Initialize a safety ticket.

        :param description: Description of the safety drill or compliance task.
        """
        self.description = description
        self.documentation = []  # List to hold documentation or checklist details.
        self.completed = False

    def add_documentation(self, doc):
        """Add documentation (e.g., checklist, report, notes) to the ticket."""
        self.documentation.append(doc)

    def complete_ticket(self):
        """Mark the safety ticket as completed."""
        self.completed = True
        print(f"Safety ticket '{self.description}' has been marked as completed.")

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return (f"Safety Ticket: {self.description}\n"
                f"Documentation: {self.documentation}\n"
                f"Status: {status}")
