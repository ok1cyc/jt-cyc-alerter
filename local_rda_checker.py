import csv

class LocalRDAChecker:
    def __init__(self, filename):
        """Initialize with the CSV filename."""
        self.filename = filename

    def get_rda_code(self, callsign):
        """
        Retrieve the RDA code for the given callsign.

        Parameters:
        - callsign (str): The callsign to look up.

        Returns:
        - str: The associated RDA code if found, else None.
        """
        try:
            # Open the file each time to ensure it reads the latest data
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                for row in reader:
                    if len(row) == 2:
                        file_callsign, rda_code = row
                        if file_callsign.strip() == callsign:
                            return rda_code.strip()
            return None  # Return None if callsign is not found
        except FileNotFoundError:
            print(f"Error: The file '{self.filename}' does not exist.")
            return None
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None