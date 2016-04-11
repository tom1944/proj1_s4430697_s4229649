"""HTTP Server

This module contains a HTTP server
"""

import socket
from threading import Thread

from webhttp import parser, composer


class ConnectionHandler(Thread):
    """Connection Handler for HTTP Server"""

    def __init__(self, conn_socket, timeout):
        """Initialize the HTTP Connection Handler

        Args:
            conn_socket (socket): socket used for connection with client
            addr (str): ip address of client
            timeout (int): seconds until timeout
        """
        super(ConnectionHandler, self).__init__()
        self.done = False
        self.daemon = True
        self.conn_socket = conn_socket
        self.timeout = timeout
        self.conn_socket.settimeout(timeout)

    def handle_connection(self):
        """Handle a new connection"""
        try:
            raw_http_requests = self.conn_socket.recv(8192)
        except socket.timeout:
            print "Connection timed out"
            self.close()
            return
        except Exception as e:
            print "Exception occurred while trying to read from socket:", e
            self.done = True
            return

        if raw_http_requests == "":  # connection has dropped
            print "Client dropped connection"
            self.done = True
            return

        http_requests = parser.parse_requests(raw_http_requests)

        for http_request in http_requests:
            print '=== request ===\n', http_request
            response = composer.compose_response(http_request)
            print "=== response ===\n", response
            self.conn_socket.send(str(response))
            try:
                if response['Connection'] == 'close':
                    self.close()
            except KeyError:
                pass

    def run(self):
        """Run the thread of the connection handler"""
        while not self.done:
            self.handle_connection()

    def close(self):
        """Close the connection"""
        self.done = True
        self.conn_socket.shutdown(socket.SHUT_RDWR)
        self.conn_socket.close()


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
            print '=== client address ===\n', address, '\n'
            ConnectionHandler(client_socket, self.timeout).start()
        server_socket.close()

    def shutdown(self):
        """Safely shut down the HTTP server"""
        self.done = True
