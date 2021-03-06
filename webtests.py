import gzip
import os
import shutil
import socket
import sys
import time
import unittest

from webhttp import message, parser

server_portnr = 8001
server_ip = "localhost"
#server_ip = "192.168.0.17"


class TestGetRequests(unittest.TestCase):
    """Test cases for GET requests
    None of these tests did succeed on our computer. We do not know what is going wrong.
    When we do these tests with a browser and listen with wireshark, everything seems fine."""
    @classmethod
    def setUpClass(cls):
        pass
        # cls.server = server.Server(server_ip, server_portnr, 15)
        # thread.start_new_thread ( cls.server.run, () )
        # time.sleep(1)  # wait for the server thread to set up the server

    @classmethod
    def tearDownClass(cls):
        pass
        # cls.server.shutdown()

    def setUp(self):
        """Prepare for testing"""
        print "setUp"
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, server_portnr))
        print "setUp done"

    def tearDown(self):
        print "tearDown"
        """Clean up after testing"""
        self.client_socket.shutdown(socket.SHUT_RDWR)
        self.client_socket.close()
        print "tearDown done"

    def test_existing_file(self):
        """GET for a single resource that exists"""
        print "test_existing_file"
        # Send the request
        request = message.Request()
        request.method = "GET"
        request.uri = "/test/index.html"
        request["Host"] = server_ip + ":{}".format(server_portnr)
        request["Connection"] = "close"
        self.client_socket.send(str(request))

        # Test response
        msg = self.client_socket.recv(1024)
        print "msg: <" + str(msg) + ">"
        response = parser.parse_response(msg)
        self.assertEqual(response.code, 200)
        print "response: <" + str(response) + ">"
        self.assertTrue(response.body)

    def test_nonexistant_file(self):
        """GET for a single resource that does not exist"""
        print "test_nonexistant_file"
        request = message.Request()
        # Send the request
        request.method = "GET"
        request.uri = "/test/doesNotExist.html"
        request["Host"] = server_ip + ":{}".format(server_portnr)
        request["Connection"] = "close"

        # Test response
        msg = self.client_socket.recv(1024)
        print "msg: <" + str(msg) + ">"
        response = parser.parse_response(msg)
        self.assertEqual(response.code, 404)
        print "response: <" + str(response) + ">"
        self.assertFalse(response.body)

    def test_caching(self):
        """GET for an existing single resource followed by a GET for that same
        resource with caching utilized on the client/tester side
        """
        print "test_caching"
        # Send the request
        request = message.Request()
        request.method = "GET"
        request.uri = "/test/index.html"
        request["Host"] = server_ip + ":{}".format(server_portnr)
        request["Connection"] = "keep-alive"
        self.client_socket.send(str(request))

        # send again with etag
        msg = self.client_socket.recv(1024)
        response = parser.parse_response(msg)
        self.assertTrue(response["ETag"])
        request["ETag"] = response["ETag"]
        request["Connection"] = "close"
        self.client_socket.send(str(request))

        # Test response
        msg = self.client_socket.recv(1024)
        print "msg: <" + str(msg) + ">"
        response = parser.parse_response(msg)
        self.assertEqual(response.code, 304)
        print "response: <" + str(response) + ">"
        self.assertFalse(response.body)

    def test_extisting_index_file(self):
        """GET for a directory with an existing index.html file"""
        print "test_extisting_index_file"
        # Send the request
        request = message.Request()
        request.method = "GET"
        request.uri = "/"
        request["Host"] = server_ip + ":{}".format(server_portnr)
        request["Connection"] = "close"
        self.client_socket.send(str(request))

        # Test response
        msg = self.client_socket.recv(1024)
        print "msg: <" + str(msg) + ">"
        response = parser.parse_response(msg)
        self.assertEqual(response.code, 200)
        print "response: <" + str(response) + ">"
        self.assertTrue(response.body)

    def test_nonexistant_index_file(self):
        """GET for a directory with a non-existant index.html file"""
        print "test_nonexistant_index_file"
        request = message.Request()
        # Send the request
        request.method = "GET"
        request.uri = "/empty"
        request["Host"] = server_ip + ":{}".format(server_portnr)
        request["Connection"] = "close"
        self.client_socket.send(str(request))

        # Test response
        msg = self.client_socket.recv(1024)
        print "msg: <" + str(msg) + ">"
        response = parser.parse_response(msg)
        self.assertEqual(response.code, 404)
        print "response: <" + str(response) + ">"
        self.assertFalse(response.body)

    def test_persistent_close(self):
        """Multiple GETs over the same (persistent) connection with the last
        GET prompting closing the connection, the connection should be closed.
        """
        print "test_persistent_close"
        request = message.Request()
        request.method = "GET"
        request.uri = "/test/index.html"
        request["Host"] = server_ip + ":{}".format(server_portnr)
        request["Connection"] = "keep-alive"

        for i in range(0,2):
            self.client_socket.send(str(request))
            msg = self.client_socket.recv(1024)

        request["Connection"] = "close"
        self.client_socket.send(str(request))
        msg = self.client_socket.recv(1024)

        time.sleep(1) # wait untill all data has been received

        self.assertRaises(socket.error, lambda: self.client_socket.send("something"))


    def test_persistent_timeout(self):
        """Multiple GETs over the same (persistent) connection, followed by a
        wait during which the connection times out, the connection should be
        closed.
        """
        print "test_persistent_timeout"
        request = message.Request()
        request.method = "GET"
        request.uri = "/test/index.html"
        request["Host"] = server_ip + ":{}".format(server_portnr)
        request["Connection"] = "keep-alive"

        for i in range(0,2):
            self.client_socket.send(str(request))
            msg = self.client_socket.recv(1024)

        self.client_socket.send(str(request))
        msg = self.client_socket.recv(1024)

        time.sleep(16)
        self.assertRaises(socket.error, lambda :self.client_socket.send("something"))

    def test_encoding(self):
        """GET which requests an existing resource using gzip encodign, which
        is accepted by the server.
        """
        print "test_encoding"
        request = message.Request()
        request.method = "GET"
        request.uri = "/test/index.html"
        request["Host"] = server_ip + ":{}".format(server_portnr)
        request["Connection"] = "keep-alive"
        request["Content-Encoding"] = "gzip"
        self.client_socket.send(str(request))

        msg = self.client_socket.recv(1024)
        response = parser.parse_response(msg)
        self.assertEqual(request["Content-Encoding"], "gzip")

        with open("/test/index.html") as content_file, gzip.open('gzip_temp', 'wb') as temp_file:
            shutil.copyfileobj(content_file, temp_file)
            content_file.close()
            temp_file.close()
        with open('gzip_temp') as temp_file:
            zipped_file = temp_file.read()
            temp_file.close()
            os.remove('gzip_temp')

        self.assertEqual(zipped_file, response.body)


if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    psr = argparse.ArgumentParser(description="HTTP Tests")
    psr.add_argument("-p", "--port", type=int, default=8001)
    
    # Arguments for the unittest framework
    psr.add_argument('unittest_args', nargs='*')
    args = psr.parse_args()
    
    # Only pass the unittest arguments to unittest
    sys.argv[1:] = args.unittest_args

    # Start test suite
    unittest.main()
