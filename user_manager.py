import hashlib
from storage.data_storage import DatabaseStorage

# Define the roles and their permissions.
ROLES = {
    "admin": {
         "permissions": ["full_control", "view", "comment", "complete_tasks", "edit_inventory", "view_safety", "view_tasks"],
         "description": "Admin has full control over everything."
    },
    "office": {
         "permissions": ["view", "comment"],
         "description": "Office can view and comment on everything."
    },
    "captain": {
         "permissions": ["view", "complete_tasks", "view_safety", "edit_inventory"],
         "description": "Captains/Mates can view and complete tasks and safety items, and view and edit inventory if allowed by admin."
    },
    "engineer": {
         "permissions": ["view", "complete_tasks", "edit_inventory", "view_safety"],
         "description": "Engineers can view and complete tasks, view and edit inventory, and view safety."
    },
    "deckhand": {
         "permissions": ["view", "view_tasks"],
         "description": "Deckhands can view inventory and tasks."
    }
}


class User:
    def __init__(self, username, role, password_hash):
        self.username = username
        self.role = role
        self.password_hash = password_hash

    def has_permission(self, permission):
        """Return True if the user's role includes the specified permission."""
        if self.role in ROLES:
            return permission in ROLES[self.role]["permissions"]
        return False

    def __str__(self):
        return f"User(username={self.username}, role={self.role})"


class UserManager:
    def __init__(self, db_storage=None):
        """
        Initialize the UserManager.
        If no database storage instance is provided, create one.
        Also, ensure that the default admin user exists.
        """
        if db_storage is None:
            self.db = DatabaseStorage()
        else:
            self.db = db_storage
        # Ensure the default admin exists.
        self.ensure_default_admin()

    def hash_password(self, password):
        """
        Hash the password using SHA-256.
        In production, consider using a more robust hashing algorithm (like bcrypt).
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password, role):
        """
        Add a new user to the system.
        Only valid roles (as defined in ROLES) will be accepted.
        """
        if role not in ROLES:
            print(f"Invalid role: {role}. User not added.")
            return
        hashed = self.hash_password(password)
        self.db.save_user(username, role, hashed)
        print(f"User '{username}' added with role '{role}'.")

    def get_user(self, username):
        """
        Retrieve a user from the storage.
        Returns a User instance if found, or None if not.
        """
        user_data = self.db.get_user(username)
        if user_data:
            return User(user_data["username"], user_data["role"], user_data["password"])
        return None

    def validate_user(self, username, password):
        """
        Validate a user's credentials.
        Returns a User instance if credentials are correct, or None otherwise.
        """
        user = self.get_user(username)
        if user and user.password_hash == self.hash_password(password):
            return user
        return None

    def update_user_role(self, username, new_role):
        """
        Update a user's role.
        Only an admin should call this function.
        """
        if new_role not in ROLES:
            print(f"Invalid role: {new_role}.")
            return False
        cursor = self.db.conn.cursor()
        cursor.execute("UPDATE users SET role = ? WHERE username = ?", (new_role, username))
        self.db.conn.commit()
        print(f"User '{username}' role updated to '{new_role}'.")
        return True

    def ensure_default_admin(self):
        """
        Ensure that a default admin exists.
        If no user with username "Josh Redden" exists, create one with password "Hunter18" and role "admin".
        """
        default_username = "Josh Redden"
        default_password = "Hunter18"
        default_role = "admin"
        if self.get_user(default_username) is None:
            print("Default admin user not found. Creating default admin user...")
            self.add_user(default_username, default_password, default_role)
        else:
            print("Default admin user already exists.")


# For testing purposes:
if __name__ == "__main__":
    um = UserManager()
    # Validate default admin credentials.
    user = um.validate_user("Josh Redden", "Hunter18")
    if user:
        print("Default admin login successful:", user)
    else:
        print("Default admin login failed.")

