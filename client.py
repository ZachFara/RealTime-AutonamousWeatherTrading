import socket
import time

# Define the server addresses and ports
servers = [("localhost", 9999), ("localhost", 8888)]  # Example: Second server on port 8888
attempt_interval = 60  # Time between attempts in seconds

# Define buoy list and a dictionary to hold the latest entries
buoy_list = [
    "44029", "44030", "JBYF1", "JCTN4", "44062", 
    "46098", "46116", "41052", "51045", "CHQO3", 
    "EAZC1", "GDQM6"
]
latest_entry = {buoy: None for buoy in buoy_list}

while True:
    for host, port in servers:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Attempt to connect to the server
                print(f"Trying to connect to {host}:{port}")
                sock.connect((host, port))
                print(f"Connected to {host}:{port}")

                # Wait for data from the server
                data = sock.recv(4096)  # Adjust buffer size as needed
                received = data.decode('utf-8')
                print(f"Received data from {host}:{port}")

                print(f"Received: {received}")

                # Process the received data
                entries = received.split("|")
                for entry in entries:
                    if len(entry) > 0:
                        details = entry.split(" ")
                        buoy_id = details[0]
                        if buoy_id in buoy_list and latest_entry[buoy_id] != entry:
                            latest_entry[buoy_id] = entry
                            print(f"Updated {buoy_id}: {entry}")

                print("====================================================================================")

        except ConnectionRefusedError:
            print(f"Connection to {host}:{port} refused. Trying the next server.")

        time.sleep(attempt_interval)  # Wait before attempting the next connection
