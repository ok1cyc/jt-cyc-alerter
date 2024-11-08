# udp_server.py
import socket
import struct
import re

class UDPServer:
    def __init__(self, ip="0.0.0.0", port=1100, header_hex="adbccbda"):
        self.udp_ip = ip
        self.udp_port = port  # Set port based on provided argument
        self.header = bytes.fromhex(header_hex)

        # Define the patterns to remove
        self.patterns_to_remove = [
            r'\bCQ\b', r'\bRR73\b', r'\bRRR\b', r'\b73\b', r'\b[A-Z]{2}[0-9]{2}\b', 
            r'\bR[+-][0-9]+\b', r'[+-][0-9]+'
        ]
        # Combine patterns into one regex
        self.combined_pattern = re.compile('|'.join(self.patterns_to_remove))

        # Set up the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))

    def start(self):
        """Generator to listen for incoming packets and yield processed callsigns."""
        print(f"Listening on UDP port {self.udp_port} for packets with '{self.header.hex()}' header.")
        while True:
            data, addr = self.sock.recvfrom(1024)
            last_word = self.process_packet(data, addr)
            if last_word and last_word != "<...>":  # Avoid yielding if last_word is "<...>"
                yield last_word  # Yield each callsign as it's processed

    def process_packet(self, data, addr):
        """Process the received packet and return the last word (callsign)."""
        if data.startswith(self.header):
            data_after_header = data[len(self.header) + 4:]
            check_value = struct.unpack(">I", data_after_header[:4])[0]
            if check_value == 2:
                remaining_data = data_after_header[4:]
                bytes_to_remove = struct.unpack(">I", remaining_data[:4])[0]
                final_data = remaining_data[4 + bytes_to_remove:]
                final_data = final_data[21:]
                next_integer = struct.unpack(">I", final_data[:4])[0]
                final_data = final_data[4 + next_integer:]
                new_integer = struct.unpack(">I", final_data[:4])[0]

                ascii_data = final_data[4:4 + new_integer]
                ascii_output = ascii_data.decode('ascii', errors='ignore')
                cleaned_output = self.combined_pattern.sub('', ascii_output)
                last_word = cleaned_output.strip().split()[-1] if cleaned_output.strip() else ''
                return last_word
        return None
