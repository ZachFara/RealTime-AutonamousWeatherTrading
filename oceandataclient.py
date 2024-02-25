import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    numbers = []
    for i in range(10):
        # Receive data from the server and shut down
        received = float(str(sock.recv(1024), "utf-8"))
        numbers.append(received)
        print(numbers[i])
print("Received: {}".format(received))
