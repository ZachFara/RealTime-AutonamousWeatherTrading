import socket
import sys
import time

HOST, PORT = "localhost", 9999

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    columns = ["Buoy", "Lat", "Long", "Month", "Day", "Hour", "Minute", "Depth", "Temp"]
    buoy_list = [
        ["44029"],
        ["44030"],
        ["JBYF1"],
        ["JCTN4"],
        ["44062"],
        ["46098"],
        ["46116"],
        ["41052"],
        ["51045"],
        ["CHQO3"],
        ["EAZC1"],
        ["GDQM6"],
    ]
    latest_entry = [" "] * 12
    # make this the number of buoys
    for i in range(10):

        received = str(sock.recv(1024), "utf-8")
        entries = received.split("|")
        for entry in entries:
            if len(entry) > 0:
                if latest_entry[buoy_list.index([entry.split(" ")[0]])] != entry:
                    latest_entry[buoy_list.index([entry.split(" ")[0]])] = entry
                    print("Updated " + entry)
        print(
            "===================================================================================="
        )
        time.sleep(1)


print("Received: {}".format(received))
