import socketserver
import yfinance as yf
import time
import math

# TODO: Fix the na values in this server

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and overrides the handle() method to implement communication to the client.
    """

    def handle(self):
        tickers = ['CORN', 'SOYB', 'WEAT', 'NG=F', 'CL=F']

        while True:
            # Download the latest data
            commodity_data = yf.download(tickers, period='1d', interval='15m')
            
            # Find the latest data point's timestamp
            latest_timestamp = max(commodity_data.index)

            # Prepare the data string to be sent
            send_str = f"Latest Data Timestamp: {latest_timestamp}\n"

            print(commodity_data.head())
            # Append each commodity's latest data to the string
            for ticker in tickers:
                try:

                    latest_data = commodity_data.loc[latest_timestamp][('Adj Close', ticker)]
                    if math.isnan(latest_data):
                        
                        ticker_data = commodity_data[('Adj Close', ticker)]
                        ticker_data = ticker_data.dropna()
                    
                        ticker_latest_timestamp = max(ticker_data.index)

                        latest_data = commodity_data.loc[ticker_latest_timestamp][('Adj Close', ticker)]
                    send_str += f"{ticker}: {latest_data}\n"
                except KeyError:
                    # In case the ticker data is missing for the latest timestamp, skip it
                    send_str += f"{ticker}: Data not available\n"
            
            # Send the data string to the client
                    
            try:
                self.request.sendall(bytes(send_str, "utf-8"))
            except BrokenPipeError:
                print("Client disconnected: Awaiting new connection...")
            

            # Wait before sending the next update
            time.sleep(1)  # Sleep for 60 seconds

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print("Server started at {}:{}".format(HOST, PORT))
        # Activate the server; this will keep running until you interrupt the program with Ctrl-C
        server.serve_forever()

