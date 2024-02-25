import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    columns = ["Buoy", "Lat", "Long", "Month", "Day", "Hour", "Minute", "Depth", "Temp"]
    # make this the number of buoys
    for i in range(12):
        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")
        print(received)

print("Received: {}".format(received))
