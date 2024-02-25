import socketserver
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        # URL of the website to scrape
        url = "https://www.ndbc.noaa.gov/data/realtime2/41064.ocean"

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the website
            soup = BeautifulSoup(response.content, "html.parser")

            # Load the text content into a pandas DataFrame
            df = pd.read_csv(
                StringIO(soup.get_text()), delim_whitespace=True, header=[0, 1]
            )

            for i in range(10):
                self.request.sendall(bytes(str(df.loc[i]["OTMP"][0]), "utf-8"))
        else:
            print("Failed to retrieve the webpage")


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
