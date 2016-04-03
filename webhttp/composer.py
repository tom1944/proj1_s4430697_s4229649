""" Composer for HTTP responses

This module contains a composer, which can compose responses to
HTTP requests from a client.
"""

import time

from webhttp import message, resource
from webhttp.resource import FileAccessError, FileExistError


def compose_response(request):
    """Compose a response to a request

    Args:
        request (webhttp.Request): request from client

    Returns:
        webhttp.Response: response to request

    """
    response = message.Response()
    response.version = 'HTTP/1.1'
    response.body = ''
    # response['Content-Length'] = 0

    if request.method == 'GET':
        response = compose_get_response(request, response)
    else:
        response = message.Response()
        response.code = 501

    if request.method == 'HTTP/1.1' and request.get_header('Connection') == 'close':
        response.set_header('Connection', 'close')
    else:
        response.set_header('Connection', 'keep-alive')

    return response


def compose_get_response(request, response):
    try:
        response.code = 200
        resource_file = resource.Resource(request.uri)
        response.body = resource_file.get_content()
        # hash = resource_file.generate_etag()
        # response.set_header("ETag", 'W"' + hash + '"')
        response.set_header('Content-Length', resource_file.get_content_length())
    except FileExistError:
        response.code = 404
    except FileAccessError:
        response.code = 403
    return response


def make_date_string():
    """Make string of date and time

    Returns:
        str: formatted string of date and time
    """
    return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
