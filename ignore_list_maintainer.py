import os

class IgnoreListMaintainer:
    def __init__(self, filename="ignore.txt"):
        self.filename = filename
        self.ignore_set = self.load_ignore_list()

    def load_ignore_list(self):
        """Load callsigns from the ignore file into a set."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return set(line.strip() for line in file if line.strip())
        return set()

    def add_callsign(self, callsign):
        """Add a new callsign to the ignore set without updating the file."""
        self.ignore_set.add(callsign)

    def is_ignored(self, callsign):
        """Check if the given callsign is in the ignore list."""
        return callsign in self.ignore_set