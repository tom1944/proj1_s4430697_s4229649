"""HTTP response and request parsers

This module contains parses for HTTP response and HTTP requests.
"""

from webhttp import message


class MessageFormatError(Exception):
    """Exception which is raised when message format is wrong"""
    pass


def parse_requests(buff):
    """Parse requests in a buffer

    Args:
        buff (str): the buffer contents received from socket

    Returns:
        list of webhttp.message.Request
    """
    requests = split_requests(buff)
    # requests = [buff]
    http_requests = []
    for request in requests:
        http_request = message.Request()

        try:
            header, body = request.split('\r\n\r\n', 1)
            http_request.body = body
        except ValueError:
            raise MessageFormatError

        lines = [x for x in header.split('\r\n') if x is not '']
        startline = lines.pop(0)
        http_request.startline = startline
        try:
            http_request.method, http_request.uri, http_request.version = startline.split()
        except ValueError:
            raise MessageFormatError

        for line in lines:
            try:
                name, value = line.split(':', 1)
                http_request.set_header(name.strip(), value.strip())
            except ValueError:
                raise MessageFormatError
        http_requests.append(http_request)
    return http_requests


def split_requests(buff):
    """Split multiple requests

    Arguments:
        buff (str): the buffer contents received from socket

    Returns:
        list of str
    """
    requests = buff.split('\r\n\r\n')
    requests = filter(None, requests)
    requests = [r + '\r\n\r\n' for r in requests]
    requests = [r.lstrip() for r in requests]
    return requests


def parse_response(buff):
    """Parse responses in buffer

    Args:
        buff (str): the buffer contents received from socket

    Returns:
        webhttp.message.Response
    """
    response = message.Response()
    return response
