""" Composer for HTTP responses

This module contains a composer, which can compose responses to
HTTP requests from a client.
"""

import time

from webhttp import message, resource, parser
from webhttp.resource import FileAccessError, FileExistError


def compose_response(request):
    """Compose a response to a request

    Args:
        request (webhttp.Request): request from client

    Returns:
        webhttp.Response: response to request

    """
    response = message.Response()

    if request.method == 'HTTP/1.1' and request['Connection'] == 'close':
        response['Connection'] = 'close'
    else:
        response['Connection'] = 'keep-alive'

    if request.method == 'GET':
        response = compose_get_response(request, response)
    else:
        response = message.Response()
        response.code = 501

    return response


def compose_get_response(request, response):
    try:
        response.code = 200
        resource_file = resource.Resource(request.uri)

        if 'gzip' in parser.parse_header(request, 'Accept-Encoding'):
            response.body = resource_file.get_content_gzip()
            response['Content-Encoding'] = 'gzip'
        else:
            response.body = resource_file.get_content()
            response['Content-Length'] = resource_file.get_content_length()

        etag = resource_file.generate_etag()
        response['ETag'] = str(etag)
        response['Date'] = make_date_string()
        response['Content-Type'] = resource_file.get_content_type()
    except FileExistError:
        response.code = 404
        response.remove_header('Connection')
    except FileAccessError:
        response.code = 403
        response.remove_header('Connection')
    return response


def make_date_string():
    """Make string of date and time

    Returns:
        str: formatted string of date and time
    """
    return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
