# test_dxcc_checker.py
from dxcc_checker import DXCCChecker

# Sample list of real or simulated amateur radio callsigns (you may use actual callsigns if available)
callsigns = [
    "DH1TW", "K1ABC", "JA2XTX", "VK4XYZ", "G0AAA", "W6BBA",
    "VE3DEF", "ZS1ABC", "PY2XYZ", "LU4AAA", "UA1AAX", "DL8USA",
    "HB9ZZZ", "ON4KST", "VK2AAA", "9A1A", "EA5BZ", "YV5ZZ",
    "OH1ABC", "SM6ABC", "F5XYZ", "I2FGT", "SP9ZZZ", "CT1AAA",
    # Add hundreds more for a comprehensive test
]

def test_dxcc_checker():
    # Initialize DXCCChecker instance (only once)
    checker = DXCCChecker()
    
    # Loop through each callsign to test
    for callsign in callsigns:
        dxcc_id = checker.get_dxcc_id(callsign)
        print(f"Callsign: {callsign}, DXCC ID: {dxcc_id}")

if __name__ == "__main__":
    test_dxcc_checker()
