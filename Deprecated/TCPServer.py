import socketserver

sockets = []

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    Server request handler

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        global sockets
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        str_data = str(self.data, 'utf-8')
        if str_data == '0':
            sockets.append(self.request)


        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        if '-1' in str_data:
            self.server.server_close()
            print("Closed")
        print(self.server.address_family)
        # just send back the same data, but upper-cased
        for socket in sockets:
            socket.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()