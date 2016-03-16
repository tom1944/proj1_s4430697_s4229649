"""HTTP response and request parsers

This module contains parses for HTTP response and HTTP requests.
"""

import webhttp.message


def parse_requests(buff):
    """Parse requests in a buffer

    Args:
        buff (str): the buffer contents received from socket

    Returns:
        list of webhttp.Request
    """
    requests = split_requests(buff)

    http_requests = []
    for request in requests:
        http_request = webhttp.message.Request()
        parse_request(request)
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
        webhttp.Response
    """
    response = webhttp.message.Response()
    return response
