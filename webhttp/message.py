"""HTTP Messages

This modules contains classes for representing HTTP responses and requests.
"""

reasondict = {
    # Dictionary for code reasons
    # Format: code : "Reason"
    200: "OK",
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
        string = ''
        startline = self.startline + '\r\n'  # " ".join([self.method, self.uri, self.version]) + "\r\n"
        string += startline
        for header in self.headerdict:
            headerline = header + ': ' + self.headerdict[header] + '\r\n'
            string += headerline
        string += '\r\n' + self.body
        return string


class Response(Message):
    """Class that stores a HTTP Response"""

    def __init__(self):
        """Initialize the Response"""
        super(Response, self).__init__()
        self.code = 500  # the status code
        self.phrase = ""  # the reason phrase
    
    def __str__(self):
        """Convert the Response to a string

        Returns:
            str: representation the can be sent over socket
        """
        self.startline = " ".join([self.version, str(self.code), self.phrase]) + "\r\n"
        headers = "\r\n".join([header + ": " + self.get_header(header) for header in self.headerdict])
        return self.startline + headers + "\r\n" + self.body
