"""HTTP Messages

This modules contains classes for representing HTTP responses and requests.
"""

reasondict = {
    # Dictionary for code reasons
    # Format: code : "Reason"
    200: "OK",
    403: "Forbidden",
    404: 'Not Found',
    500: "Internal Server Error",
    501: "Not Implemented"
}


class Message(object):
    """Class that stores a HTTP Message"""

    def __init__(self):
        """Initialize the Message"""
        self.version = "HTTP/1.1"
        self.body = ""
        self.headerdict = dict()

    def __getitem__(self, name):
        """Alternative method to get header"""
        if name in self.headerdict:
            return self.headerdict[name]
        else:
            return ''

    def __setitem__(self, name, value):
        """Alternative method to set header"""
        self.headerdict[name] = value

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
            return ''


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
        startline = " ".join([self.method, self.uri, self.version]) + "\r\n"
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
        self.phrase = ''  # the response phrase
    
    def __str__(self):
        """Convert the Response to a string

        Returns:
            str: representation the can be sent over socket
        """
        phrase = reasondict[self.code] if self.phrase == '' else self.phrase
        startline = " ".join([self.version, str(self.code), phrase]) + "\r\n"
        headers = [header + ": " + str(self[header]) + '\r\n' for header in self.headerdict]
        return startline + "".join(headers) + "\r\n" + self.body
