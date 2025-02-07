#!/usr/bin/env python3
"""
Main entry point for the Tugboat Inventory and Ticketing System.

This file integrates:
  - Inventory management (via TugboatInventory)
  - Ticketing (MaintenanceTicket, SafetyTicket, RecurringTicket)
  - Role-Based Access & Audit Trails (via utils/security)
  - Notifications and automated alerts (via utils/notifications)
  - Advanced Reporting (via utils/reports)
  - Database storage (via storage/data_storage)
  - GUI login (via ui/login) and GUI main menu (via ui/main_menu)
"""

import sys
from datetime import datetime

# Import inventory modules
from inventory.manager import TugboatInventory

# Import ticketing modules
from tickets.maintenance import MaintenanceTicket
from tickets.safety import SafetyTicket
try:
    from tickets.recurring import RecurringTicket, process_recurring_tickets
except ImportError:
    RecurringTicket = None
    process_recurring_tickets = None

# Import security/ audit modules
from utils.security import log_event

# Import notifications module
from utils.notifications import process_inventory_alerts

# Import reporting module
from utils.reports import generate_usage_report, generate_inventory_report, print_usage_report, print_inventory_report

# Import storage module
from storage.data_storage import DatabaseStorage

# Import GUI login and main menu functions
from ui.login import run_login
from ui.main_menu import run_main_menu

# -------------------- Global Setup --------------------

# Instantiate the inventory manager and database storage
inventory_manager = TugboatInventory()
db_storage = DatabaseStorage()

# For demonstration, add some tugboats (in a real system these might be loaded from the database)
tugboats = [
    "Anne Jarrett", "Beaufort", "Belle", "Captain D", "George Holland",
    "Jack Holland", "James William", "Lorette", "Pamlico", "Pathfinder",
    "Paula Atwell", "Robert Burton", "Stephen J. Leaman",
    "W. Lloyd Taliaferro", "Ware House"
]
for tugboat in tugboats:
    inventory_manager.add_tugboat(tugboat)

# Sample list for recurring tickets (if using recurring tickets)
recurring_tickets = []

# We will use the GUI login instead of a CLI demo user dictionary.
current_user = None

# -------------------- Login Function (GUI) --------------------

def login_via_gui():
    global current_user
    print("Launching GUI login window...")
    current_user = run_login()  # run_login() will display the login window and return the authenticated user.
    if current_user is None:
        print("Login failed. Exiting.")
        sys.exit(1)
    else:
        log_event(current_user, "Login", f"User {current_user.username} logged in.")
        print(f"Welcome, {current_user.username}! Your role is: {current_user.role}")

# -------------------- Main Program --------------------

def main():
    # Launch the GUI login window and authenticate the user.
    login_via_gui()
    # After successful login, call the GUI main menu.
    run_main_menu(current_user)
    # Close the database connection when done.
    db_storage.close()

if __name__ == '__main__':
    main()
