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

    if request.method == 'GET':
        response = compose_get_response(request, response)
    else:
        response.code = 501

    if response.code == 200:
        if request.method == 'HTTP/1.1' and request['Connection'] == 'close':
            response['Connection'] = 'close'
        else:
            response['Connection'] = 'keep-alive'

    return response


def compose_get_response(request, response):
    try:
        response.code = 200
        resource_file = resource.Resource(request.uri)
        etag = resource_file.generate_etag()

        if request['If-None-Match'] == etag:
            response.code = 304
            return response
        response['ETag'] = str(etag)

        if 'gzip' in parser.parse_header(request, 'Accept-Encoding'):
            response.body = resource_file.get_content_gzip()
            response['Content-Encoding'] = 'gzip'
            response['Content-Length'] = len(response.body)
        else:
            response.body = resource_file.get_content()
            response['Content-Length'] = resource_file.get_content_length()

        response['Date'] = make_date_string()
        response['Content-Type'] = resource_file.get_content_type()
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
