import socket
import time
import threading
import csv
from io import StringIO

# Define the server addresses and ports
servers = [
    ("localhost", 9999),
    ("localhost", 8888),
]  # Example: Second server on port 8888
attempt_interval = 15  # Time between attempts in seconds

# Define buoy list and a dictionary to hold the latest entries
buoy_list = [
    "44029",
    "44030",
    "JBYF1",
    "JCTN4",
    "44062",
    "46098",
    "46116",
    "41052",
    "51045",
    "CHQO3",
    "EAZC1",
    "GDQM6",
]
symbol_list = ["CORN", "SOYB", "WEAT", "NG=F", "CL=F"]
latest_entry = {buoy: None for buoy in buoy_list}
latest_entry.update({symbol: None for symbol in symbol_list})
latest_entry.update({"Latest Data Timestamp": None})
ocean_change = 0
lock = threading.Lock()
# Signals are generated through future price connection
signal_list = []

def process_signals(signal,prev_signal):
    
    if signal == 1:
        if prev_signal == 1:
            return "Hold"
        else:
            return "Buy"
    elif signal == -1:
        return "Sell"
    else: # signal == 0
        return "Sell"

# Profit and loss book based on what price we bought and sold at
from PnLBook import PnLBook
book = PnLBook(verbose = 1)

def connect_to_server(host, port):
    global ocean_change
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            try:
                # Attempt to connect to the server
                print(f"Trying to connect to {host}:{port}")
                print(f"Connected to {host}:{port}")

                # Wait for data from the server
                data = sock.recv(4096)  # Adjust buffer size as needed
                received = data.decode("utf-8")
                print(f"Received data from {host}:{port}")
                print(f"Received: {received}")

                if port == 9999:  # Stock data
                    data_file = StringIO(received)

                    time_updated = False

                    # Read each line from the file-like object
                    for line in data_file:
                        # Split each line at the colon (":")
                        parts = line.strip().split(":")
                        # Extract the symbol and value
                        symbol = parts[0]
                        value = parts[1].strip()

                        if (
                            symbol == "Latest Data Timestamp"
                            and value != latest_entry.get("Latest Data Timestamp", " ")
                        ):
                            time_updated = True

                        # Updates the signal
                        if (
                            latest_entry.get(symbol)
                            and symbol != "Latest Data Timestamp"
                        ):

                            change = float(value) - float(latest_entry[symbol])
                            if change > 0 and ocean_change < 0:
                                signal_list.append([symbol, value, -1])
                            elif change < 0 and ocean_change > 0:
                                signal_list.append([symbol, value, 1])
                            else:
                                signal_list.append([symbol, value, 0])

                            # Process the signals here
                            if len(signal_list) > 1:
                                order = process_signals(signal_list[-1][2],signal_list[-2][2])
                                if order == "Buy":
                                    book.buy(symbol, float(value))
                                elif order == "Sell":
                                    book.sell(symbol, float(value))
                                else:
                                    print(f"Holding {symbol} at {value}")

                        latest_entry[symbol] = value

                        if time_updated:
                            with lock:
                                ocean_change = 0
                                print(
                                    "Time updated, ocean change is " + str(ocean_change)
                                )

                        # Updates every 5 mins (5 symbols every 15 seconds)
                        if len(signal_list) % 100 == 0:
                            with open(
                                "signals_" + str(len(signal_list) / 100) + ".csv",
                                "w",
                                newline="",
                            ) as f:
                                writer = csv.writer(f)
                                writer.writerows(signal_list)

                if port == 8888:  # Ocean data
                    # Process the received data
                    entries = received.split("|")
                    total_change = 0
                    for entry in entries:
                        if len(entry) > 0:
                            details = entry.split(" ")
                            buoy_id = details[0]
                            if buoy_id in buoy_list and latest_entry[buoy_id] != entry:
                                if latest_entry[buoy_id] and entry != " ":
                                    total_change += float(details[8]) - float(
                                        latest_entry[buoy_id].split(" ")[8]
                                    )
                                latest_entry[buoy_id] = entry
                                print(f"Updated {buoy_id}: {entry}")
                                with lock:
                                    ocean_change += total_change
                    print(ocean_change)

                    print(
                        "===================================================================================="
                    )

            ##### IMPLEMENT THE TRADING HERE

            except ConnectionRefusedError:
                print(f"Connection to {host}:{port} refused. Trying the next server.")

            time.sleep(attempt_interval)


# Create and start a separate thread for each server
for host, port in servers:
    thread = threading.Thread(target=connect_to_server, args=(host, port))
    thread.start()
