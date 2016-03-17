"""HTTP Messages

This modules contains classes for representing HTTP responses and requests.
"""

reasondict = {
    # Dictionary for code reasons
    # Format: code : "Reason"
    500: "Internal Server Error"
}


class Message(object):
    """Class that stores a HTTP Message"""

    def __init__(self):
        """Initialize the Message"""
        self.version = "HTTP/1.1"
        self.startline = ""
        self.body = ""
        self.headerdict = dict()
        
    def set_header(self, name, value):
        """Add a header and its value
        
        Args:
            name (str): name of header
            value (str): value of header
        """
        self.headerdict[name] = value
        
    def get_header(self, name):
        """Get the value of a header
        
        Args:
            name (str): name of header

        Returns:
            str: value of header, empty if header does not exist
        """
        if name in self.headerdict:
            return self.headerdict[name]
        else:
            return ""

    def set_body(self, body):
        self.body = body

    def get_body(self):
        return self.body

    def set_version(self, version):
        self.version = version

    def get_version(self):
        return self.version

    def __str__(self):
        """Convert the Message to a string
        
        Returns:
            str: representation the can be sent over socket
        """
        message = ""
        return message


class Request(Message):
    """Class that stores a HTTP request"""

    def __init__(self, ):
        """Initialize the Request"""
        super(Request, self).__init__()
        self.method = ""
        self.uri = ""
        
    def __str__(self):
        """Convert the Request to a string

        Returns:
            str: representation the can be sent over socket
        """
        startline = [ self.method, self.uri, self.version].join(" ") + "\r\n"
        return ""

    def set_method(self, method):
        self.method = method

    def get_method(self):
        return self.method

    def set_request_uri(self, uri):
        self.uri = uri

    def get_request_uri(self):
        return self.uri

class Response(Message):
    """Class that stores a HTTP Response"""

    def __init__(self):
        """Initialize the Response"""
        super(Response, self).__init__()
        self.code = 500
    
    def __str__(self):
        """Convert the Response to a string

        Returns:
            str: representation the can be sent over socket
        """
        self.startline = ""                                      
        return super(Response, self).__str__()

    def set_status_code(self, code):
        self.code = code

    def get_status_code(self):
        return self.code