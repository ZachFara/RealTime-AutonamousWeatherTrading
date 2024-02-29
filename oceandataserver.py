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
        # buoy string with lat + long
        buoy_list = [
            ["44029", 42.523, 70.566],
            ["44030", 43.179, 70.426],
            ["JBYF1", 25.224, 80.541],
            ["JCTN4", 39.508, 74.338],
            ["44062", 38.556, 76.415],
            ["46098", 44.378, 124.947],
            ["46116", 46.287, 124.016],
            ["41052", 18.249, 64.763],
            ["51045", 19.734, 155.082],
            ["CHQO3", 43.282, 124.320],
            ["EAZC1", 36.846, 121.754],
            ["GDQM6", 30.357, 88.463],
        ]
        while True:
            for buoy in buoy_list:
                # URL of the website to scrape
                url = "https://www.ndbc.noaa.gov/data/realtime2/" + buoy[0] + ".ocean"

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
                    send_str = [
                        str(buoy[0]),
                        str(buoy[1]),
                        str(buoy[2]),
                        str(df.loc[0]["MM"][0]),
                        str(df.loc[0]["DD"][0]),
                        str(df.loc[0]["hh"][0]),
                        str(df.loc[0]["mm"][0]),
                        str(df.loc[0]["DEPTH"][0]),
                        str(df.loc[0]["OTMP"][0]),
                    ]
                    send_str = " ".join(send_str)
                    
                    try:
                        self.request.sendall(bytes(send_str, "utf-8"))
                    except BrokenPipeError:
                        print("Client disconnected: Awaiting new connection...")
                else:
                    print("Failed to retrieve the webpage")
            time.sleep(15)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8888

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
