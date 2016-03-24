""" Composer for HTTP responses

This module contains a composer, which can compose responses to
HTTP requests from a client.
"""

import time

from webhttp import message, resource
from webhttp.resource import FileAccessError, FileExistError


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
        if request.method == 'GET':
            return self.compose_get_response(request)
        else:
            response = message.Response()
            response.code = 501
            return response

    def compose_get_response(self, request):
        response = message.Response()
        response.version = 'HTTP/1.1'
        try:
            response.code = 200
            resource_file = resource.Resource(request.uri)
            response.body = resource_file.get_content()
        except FileExistError:
            response.code = 404
        except FileAccessError:
            response.code = 403

        return response

    def make_date_string(self):
        """Make string of date and time
        
        Returns:
            str: formatted string of date and time
        """
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
