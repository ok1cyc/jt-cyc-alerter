from bs4 import BeautifulSoup
import requests
import re

class RDAChecker:
    def __init__(self):
        pass  # No initialization is required here

    def get_rda(self, callsign):
        """
        Fetches the RDA/URDA code for the given callsign.
        Returns the RDA code as a string if found, or 0 if not.
        """
        try:
            url = f"https://qrz.ru/db/{callsign}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for failed requests
            soup = BeautifulSoup(response.text, 'html.parser')

            # Search for RDA/URDA information in the divs
            for div in soup.find_all("div"):
                if "RDA/URDA" in div.get_text():
                    rda_info = div.get_text().strip()
                    match = re.search(r'RDA/URDA #(\w+-\d+)', rda_info)
                    if match:
                        return match.group(1)  # Return the RDA code if found

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {callsign}: {e}")

        return 0  # Return 0 if RDA/URDA information is not found
