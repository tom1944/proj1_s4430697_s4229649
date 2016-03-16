"""HTTP Server

This module contains a HTTP server
"""

import socket
import threading


class ConnectionHandler(threading.Thread):
    """Connection Handler for HTTP Server"""

    def __init__(self, conn_socket, addr, timeout):
        """Initialize the HTTP Connection Handler

        Args:
            conn_socket (socket): socket used for connection with client
            addr (str): ip address of client
            timeout (int): seconds until timeout
        """
        super(ConnectionHandler, self).__init__()
        self.daemon = True
        self.conn_socket = conn_socket
        self.addr = addr
        self.timeout = timeout

    def handle_connection(self):
        """Handle a new connection"""
        raw_http_requests = self.conn_socket.recv(20)
        http_requests = parse_request(raw_http_requests)

        print(http_request)

        self.conn_socket.close()

    def run(self):
        """Run the thread of the connection handler"""
        self.handle_connection()


class Server:
    """HTTP Server"""

    def __init__(self, hostname, server_port, timeout):
        """Initialize the HTTP server

        Args:
            hostname (str): hostname of the server
            server_port (int): port that the server is listening on
            timeout (int): seconds until timeout
        """
        self.hostname = hostname
        self.server_port = server_port
        self.timeout = timeout
        self.done = False

    def run(self):
        """Run the HTTP Server and start listening"""
        server_socket = socket.socket()
        server_socket.bind((self.hostname, self.server_port))
        server_socket.listen(5)
        while not self.done:
            (client_socket, address) = server_socket.accept()
            print(address)
            connection = ConnectionHandler(client_socket, address, self.timeout)
            connection.run()

    def shutdown(self):
        """Safely shut down the HTTP server"""
        self.done = True