from pyhamtools import LookupLib, Callinfo
import re

class QRZChecker:
    def __init__(self):
        # Initialize the lookup library only once when the instance is created
        self.lookuplib = LookupLib(lookuptype="qrz", username="ok1cyc", pwd="swlamigo")
        self.callinfo = Callinfo(self.lookuplib)

    def get_all(self, callsign):
        """
        Returns all info for the given callsign.
        If the callsign is not found, returns 0.
        """
        try:
            info = self.callinfo.get_all(callsign)
            return info if info is not None else 0  # Return 0 if not found
        except Exception as e:
            print(f"Error retrieving info for {callsign}: {e}")
            return 0  # Return 0 on error

    @staticmethod
    def get_EAprovince(callsign):
        """
        Calls get_all internally and extracts the province code from the zipcode.
        If zipcode is not provided, checks addr2 for a sequence of 5 digits.

        Parameters:
        - callsign (str): The callsign for which to retrieve the information.
        
        Returns:
        - str: The first two digits of the zipcode (or found 5-digit sequence in addr2).
        """
        checker = QRZChecker()
        all_data = checker.get_all(callsign)  # Get all info for the callsign
        if all_data != 0:
            zipcode = all_data.get('zipcode', '')
            if zipcode:
                if len(zipcode) >= 2:
                    return zipcode[:2]  # Return first two digits of zipcode
            else:
                # If no zipcode, check addr2 for a 5-digit sequence
                addr2 = all_data.get('addr2', '')
                if addr2:
                    match = re.search(r'\d{5}', addr2)  # Look for 5 digits in a row
                    if match:
                        return match.group(0)[:2]  # Return first two digits of the found sequence
        return None  # Return None if no valid data or zipcode found
