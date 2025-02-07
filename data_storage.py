import sqlite3
import json
from datetime import datetime

DB_FILE = "tugboat_system.db"

class DatabaseStorage:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row  # allows dictionary-like access to rows
        self.initialize_db()

    def initialize_db(self):
        """Create tables for inventory, tickets, users, and audit logs if they do not exist."""
        cursor = self.conn.cursor()
        # Inventory Items Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tugboat_name TEXT NOT NULL,
                item_number TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                location TEXT,
                unit TEXT,
                vendor TEXT,
                min_stock INTEGER,
                safety_stock INTEGER,
                expiry_date TEXT,
                image_path TEXT,
                documents TEXT,         -- JSON string of document paths/URLs
                category TEXT,
                cost REAL,
                quantity INTEGER,
                usage_history TEXT,     -- JSON string of usage records
                maintenance_records TEXT,  -- JSON string of maintenance records
                alert_active INTEGER    -- 0 (False) or 1 (True)
            )
        """)
        # Tickets Table (for both maintenance and safety tickets)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,              -- 'maintenance' or 'safety'
                tugboat_name TEXT,
                description TEXT,
                required_items TEXT,    -- JSON string (e.g., {"Wrench": 2, "Oil": 1})
                comments TEXT,          -- JSON string of comments
                completed INTEGER       -- 0 (False) or 1 (True)
            )
        """)
        # Users Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                role TEXT,
                password TEXT           -- In a real application, store hashed passwords
            )
        """)
        # Audit Logs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                username TEXT,
                role TEXT,
                action TEXT,
                details TEXT
            )
        """)
        self.conn.commit()

    # -------------------- Inventory Methods --------------------

    def save_inventory_item(self, tugboat_name, item):
        """
        Save or update an inventory item.
        'item' should be an instance of your InventoryItem class.
        It converts JSON-serializable fields (usage_history, maintenance_records, documents) accordingly.
        """
        cursor = self.conn.cursor()
        usage_history_json = json.dumps(item.usage_history)
        maintenance_records_json = json.dumps(item.maintenance_records)
        documents_json = json.dumps(item.documents)
        expiry_date_str = item.expiry_date.strftime("%Y-%m-%d") if item.expiry_date else None

        # Check if the item already exists for the tugboat (by item_number)
        cursor.execute("""
            SELECT id FROM inventory_items 
            WHERE tugboat_name = ? AND item_number = ?
        """, (tugboat_name, item.item_number))
        result = cursor.fetchone()

        if result:
            # Update existing item
            cursor.execute("""
                UPDATE inventory_items
                SET name = ?,
                    description = ?,
                    location = ?,
                    unit = ?,
                    vendor = ?,
                    min_stock = ?,
                    safety_stock = ?,
                    expiry_date = ?,
                    image_path = ?,
                    documents = ?,
                    category = ?,
                    cost = ?,
                    quantity = ?,
                    usage_history = ?,
                    maintenance_records = ?,
                    alert_active = ?
                WHERE id = ?
            """, (item.name, item.description, item.location, item.unit, item.vendor,
                  item.min_stock, item.safety_stock, expiry_date_str, item.image_path,
                  documents_json, item.category, item.cost, item.quantity, usage_history_json,
                  maintenance_records_json, int(item.alert_active), result['id']))
        else:
            # Insert new item
            cursor.execute("""
                INSERT INTO inventory_items (
                    tugboat_name, item_number, name, description, location, unit, vendor,
                    min_stock, safety_stock, expiry_date, image_path, documents, category,
                    cost, quantity, usage_history, maintenance_records, alert_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (tugboat_name, item.item_number, item.name, item.description, item.location,
                  item.unit, item.vendor, item.min_stock, item.safety_stock, expiry_date_str,
                  item.image_path, documents_json, item.category, item.cost, item.quantity,
                  usage_history_json, maintenance_records_json, int(item.alert_active)))
        self.conn.commit()

    def get_inventory_items(self, tugboat_name):
        """
        Retrieve all inventory items for a specific tugboat.
        Returns a list of dictionaries representing each item.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM inventory_items WHERE tugboat_name = ?
        """, (tugboat_name,))
        rows = cursor.fetchall()
        items = []
        for row in rows:
            item_dict = dict(row)
            # Convert JSON strings back into Python objects
            item_dict['usage_history'] = json.loads(item_dict['usage_history']) if item_dict['usage_history'] else []
            item_dict['maintenance_records'] = json.loads(item_dict['maintenance_records']) if item_dict['maintenance_records'] else []
            item_dict['documents'] = json.loads(item_dict['documents']) if item_dict['documents'] else []
            items.append(item_dict)
        return items

    # -------------------- Ticket Methods --------------------

    def save_ticket(self, ticket):
        """
        Save a ticket (maintenance or safety) to the database.
        'ticket' is expected to be a dictionary with keys: type, tugboat_name, description,
        required_items (dict), comments (list), and completed (boolean).
        """
        cursor = self.conn.cursor()
        required_items_json = json.dumps(ticket.get('required_items', {}))
        comments_json = json.dumps(ticket.get('comments', []))
        cursor.execute("""
            INSERT INTO tickets (type, tugboat_name, description, required_items, comments, completed)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (ticket.get('type'),
              ticket.get('tugboat_name'),
              ticket.get('description'),
              required_items_json,
              comments_json,
              int(ticket.get('completed', False))))
        self.conn.commit()

    def get_tickets(self, ticket_type=None):
        """
        Retrieve tickets from the database.
        Optionally, filter by ticket_type ('maintenance' or 'safety').
        Returns a list of ticket dictionaries.
        """
        cursor = self.conn.cursor()
        if ticket_type:
            cursor.execute("SELECT * FROM tickets WHERE type = ?", (ticket_type,))
        else:
            cursor.execute("SELECT * FROM tickets")
        rows = cursor.fetchall()
        tickets = []
        for row in rows:
            ticket = dict(row)
            ticket['required_items'] = json.loads(ticket['required_items']) if ticket['required_items'] else {}
            ticket['comments'] = json.loads(ticket['comments']) if ticket['comments'] else []
            tickets.append(ticket)
        return tickets

    # -------------------- User Methods --------------------

    def save_user(self, username, role, password):
        """
        Save a new user.
        'password' should be hashed in a production system.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, role, password)
                VALUES (?, ?, ?)
            """, (username, role, password))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"User {username} already exists.")

    def get_user(self, username):
        """Retrieve a user by username."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM users WHERE username = ?
        """, (username,))
        row = cursor.fetchone()
        return dict(row) if row else None

    # -------------------- Audit Log Methods --------------------

    def log_audit_event(self, username, role, action, details):
        """
        Log an audit event.
        'details' can be any string (or JSON string) describing the event.
        """
        cursor = self.conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO audit_logs (timestamp, username, role, action, details)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, username, role, action, str(details)))
        self.conn.commit()

    def get_audit_logs(self):
        """Retrieve all audit log entries, ordered by timestamp descending."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    # -------------------- General Methods --------------------

    def close(self):
        """Close the database connection."""
        self.conn.close()


# Example usage (for testing purposes)
if __name__ == "__main__":
    # Instantiate the database storage
    db = DatabaseStorage()

    # Example: Save a dummy inventory item
    # (Assuming you have an InventoryItem class imported from your models)
    try:
        from inventory.models import InventoryItem
    except ImportError:
        # For testing purposes, if the actual InventoryItem is not available,
        # define a simple dummy version.
        class InventoryItem:
            def __init__(self, item_number, name, quantity=0):
                self.item_number = item_number
                self.name = name
                self.description = "Test Description"
                self.location = "Test Location"
                self.unit = "each"
                self.vendor = "Test Vendor"
                self.min_stock = 10
                self.safety_stock = 5
                self.expiry_date = None
                self.image_path = None
                self.documents = []
                self.category = "Test Category"
                self.cost = 10.0
                self.quantity = quantity
                self.usage_history = []
                self.maintenance_records = []
                self.alert_active = False

    # Create a dummy inventory item and save it
    dummy_item = InventoryItem(item_number="A123", name="Test Widget", quantity=8)
    db.save_inventory_item("Test Tugboat", dummy_item)

    # Retrieve and print inventory items for the tugboat
    items = db.get_inventory_items("Test Tugboat")
    print("Retrieved Inventory Items:")
    for item in items:
        print(item)

    # Log an audit event
    db.log_audit_event("admin", "admin", "Test Action", "This is a test audit event.")

    # Retrieve and print audit logs
    audit_logs = db.get_audit_logs()
    print("\nAudit Logs:")
    for log in audit_logs:
        print(log)

    # Close the database connection when done
    db.close()
