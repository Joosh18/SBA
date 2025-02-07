# utils/notifications.py

import smtplib
from email.mime.text import MIMEText


def send_email_alert(subject, message, recipients):
    """
    Send an email alert to the specified recipients.
    Currently, this function prints the alert details.
    To send real emails, configure the SMTP settings below.
    """
    print("Sending email alert:")
    print("Subject:", subject)
    print("Message:", message)
    print("Recipients:", recipients)

    # Uncomment and configure the following to enable actual email sending:
    """
    sender = "your_email@example.com"
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)

    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login("your_username", "your_password")
            server.sendmail(sender, recipients, msg.as_string())
    except Exception as e:
        print("Failed to send email:", e)
    """


def process_inventory_alerts(inventory_manager, email_recipients):
    """
    Iterate over all inventory items across tugboats. For each item that
    needs reordering (i.e., its quantity is at or below the threshold defined
    by min_stock and safety_stock), send an email alert (if not already sent)
    and mark the item with alert_active. If an item is restocked above the threshold,
    clear the alert flag.

    Returns a list of active alerts for GUI display.
    Each alert is a tuple: (tugboat_name, item)
    """
    alerts = []
    for tugboat, items in inventory_manager.inventory.items():
        for item_number, item in items.items():
            if item.check_reorder():
                if not item.alert_active:
                    subject = f"Inventory Alert: {item.name} on {tugboat}"
                    message = (
                        f"Item {item.name} (Item Number: {item.item_number}) on tugboat '{tugboat}' "
                        f"is below its reorder threshold.\n"
                        f"Current Quantity: {item.quantity}\n"
                        f"Minimum Stock: {item.min_stock} | Safety Stock: {item.safety_stock}\n"
                        "Please reorder as soon as possible."
                    )
                    send_email_alert(subject, message, email_recipients)
                    item.alert_active = True
                alerts.append((tugboat, item))
            else:
                if item.alert_active:
                    # Clear the alert if the item is restocked above its threshold.
                    item.alert_active = False
    return alerts


def get_active_alerts(inventory_manager):
    """
    Return a list of current active alerts for GUI notifications.
    Each alert is a tuple: (tugboat_name, item)
    """
    alerts = []
    for tugboat, items in inventory_manager.inventory.items():
        for item_number, item in items.items():
            if item.check_reorder():
                alerts.append((tugboat, item))
    return alerts
