""" Composer for HTTP responses

This module contains a composer, which can compose responses to
HTTP requests from a client.
"""

import time

from webhttp import message, resource


class ResponseComposer:
    """Class that composes a HTTP response to a HTTP request"""

    def __init__(self, timeout):
        """Initialize the ResponseComposer
        
        Args:
            timeout (int): connection timeout
        """
        self.timeout = timeout
    
    def compose_response(self, request):
        """Compose a response to a request
        
        Args:
            request (webhttp.Request): request from client

        Returns:
            webhttp.Response: response to request

        """
        if request.type == 'GET':
            return self.compose_get_response()

    def compose_get_response(self):
        response = message.Response()

        return response

    def make_date_string(self):
        """Make string of date and time
        
        Returns:
            str: formatted string of date and time
        """
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
