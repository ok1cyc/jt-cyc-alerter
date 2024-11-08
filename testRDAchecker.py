# test_rda_checker.py
from rda_checker import RDAChecker

def test_rda_checker(callsign):
    rda_checker = RDAChecker(callsign)
    rda_code = rda_checker.get_rda()
    if rda_code != 0:
        print(f"The RDA code for the callsign '{callsign}' is: {rda_code}")
    else:
        print(f"No RDA code found for the callsign '{callsign}'.")

if __name__ == "__main__":
    # Test with a known callsign (replace 'ra3lbk' with a callsign you want to test)
    test_rda_checker("ua3sid")  # Replace with a valid callsign to check
