# utils/security.py

import datetime

# Define roles and their permissions.
ROLES = {
    'admin': {
        'permissions': ['view', 'modify', 'delete', 'audit', 'report']
    },
    'manager': {
        'permissions': ['view', 'modify', 'report']
    },
    'crew': {
        'permissions': ['view']
    }
}


class User:
    def __init__(self, username, role):
        if role not in ROLES:
            raise ValueError(f"Invalid role: {role}. Valid roles are: {list(ROLES.keys())}")
        self.username = username
        self.role = role

    def has_permission(self, permission):
        """Return True if the user’s role includes the specified permission."""
        return permission in ROLES[self.role]['permissions']


# Global audit log list; in production, consider logging to a file or database.
audit_log = []


def log_event(user, action, details):
    """
    Log an audit event.

    :param user: A User instance performing the action (or None for system events).
    :param action: A string describing the action (e.g., "Added item", "Removed inventory").
    :param details: A string or dict with additional details about the event.
    """
    event = {
        'timestamp': datetime.datetime.now().isoformat(),
        'username': user.username if user else "System",
        'role': user.role if user else "System",
        'action': action,
        'details': details
    }
    audit_log.append(event)
    # For demonstration, we print the event. In a real system, write to persistent storage.
    print("Audit Log Event:", event)


def get_audit_log():
    """Return the current audit log."""
    return audit_log
