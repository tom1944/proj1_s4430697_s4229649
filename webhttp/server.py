"""HTTP Server

This module contains a HTTP server
"""

import socket
import threading

from webhttp import parser, composer


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
        raw_http_requests = self.conn_socket.recv(8192)
        http_requests = parser.parse_requests(raw_http_requests)

        for http_request in http_requests:
            print(http_request)
            comp = composer.ResponseComposer(self.timeout)
            response = comp.compose_response(http_request)
            self.conn_socket.send(str(response))

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
        server_socket.listen(20)
        while not self.done:
            (client_socket, address) = server_socket.accept()
            connection = ConnectionHandler(client_socket, address, self.timeout)
            connection.run()
        server_socket.close()

    def shutdown(self):
        """Safely shut down the HTTP server"""
        self.done = True
