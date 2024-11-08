import os
from datetime import datetime, timedelta

class AlertListMaintainer:
    def __init__(self, filename="alert.txt"):
        self.filename = filename
        self.alerts = self.load_alerts()

    def load_alerts(self):
        """Load callsigns from the alert file into a dictionary with 'Static alert' and their timestamps."""
        alerts_dict = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    callsign = line.strip()
                    if callsign:  # Ensure callsign is not empty
                        alerts_dict[callsign] = (f"{callsign} - Static alert", datetime.now())  # Store with "Static alert" and current datetime
        return alerts_dict

    def is_alerted(self, callsign):
        """Check if the given callsign is in the alerts."""
        return callsign in self.alerts 

    def add_callsign(self, callsign, message):
        """Add or update a callsign in the alerts with the given message and current timestamp."""
        self.alerts[callsign] = (message, datetime.now())  # Overwrite if already exists

    def get_data(self, callsign):
        """Get all data associated with the given callsign."""
        if callsign in self.alerts:
            return self.alerts[callsign]  # Returns (message, timestamp)
        return None  # Return None if callsign is not found

    def increase_timestamp(self, callsign, minutes):
        """Increase the timestamp for the given callsign by the specified number of minutes."""
        if callsign in self.alerts:
            message, _ = self.alerts[callsign]  # Get the current message
            new_timestamp = datetime.now() + timedelta(minutes=minutes)  # Calculate new timestamp
            self.alerts[callsign] = (message, new_timestamp)  # Update with new timestamp
            print(f"Callsign '{callsign}' alerted next time at {new_timestamp}")
            return True  # Indicate success
        return False  # Indicate failure if callsign is not found
