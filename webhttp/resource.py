"""Resources

This module contains a handler class for resources.
"""

import hashlib
import mimetypes
import os
import urlparse
import gzip
import shutil


class FileExistError(Exception):
    """Exception which is raised when file does not exist"""
    pass


class FileAccessError(Exception):
    """Exception which is raised when file exists, but cannot be accessed"""
    pass


class Resource:
    """Class for representing a Resource (file)"""

    def __init__(self, uri):
        """Initialize the resource"

        Raises:
            FileExistError: if resource does not exist
            FileAccessError: if resource exists, but cannot be accessed

        Args:
            uri (str): Uniform Resource Identifier
        """
        self.uri = uri
        out = urlparse.urlparse(uri)
        self.path = os.path.join("content", out.path.lstrip("/"))
        if os.path.isdir(self.path):
            self.path = os.path.join(self.path, "index.html")
        if not os.path.isfile(self.path):
            raise FileExistError
        if not os.access(self.path, os.R_OK):
            raise FileAccessError

    def generate_etag(self):
        """Generate the ETag for the resource

        Returns:
            str: ETag for the resource
        """
        content = self.get_content()
        etag = hashlib.md5(content).hexdigest()
        return etag

    def time_modified(self):
        stat = os.stat(self.path)
        return stat.st_mtime

    def get_content(self):
        """Get the contents of the resource
        
        Returns:
            str: Contents of the resource
        """
        with open(self.path) as content_file:
            content = content_file.read()
            content_file.close()
        return content

    def get_content_gzip(self):
        """Get the contents of the resource

        Returns:
            str: Contents of the resource
        """
        with open(self.path) as content_file, gzip.open('gzip_temp', 'wb') as temp_file:
            shutil.copyfileobj(content_file, temp_file)
            content_file.close()
            temp_file.close()
        with open('gzip_temp') as temp_file:
            content = temp_file.read()
            temp_file.close()
            os.remove('gzip_temp')
        return content
        # return zlib.compress(self.get_content())

    def get_content_type(self):
        """Get the content type, i.e "text/html"

        Returns:
            str: type of content in the resource
        """
        mimetype = mimetypes.guess_type(self.path)
        return mimetype[0]

    def get_content_encoding(self):
        """Get the content encoding, i.e "gzip"

        Returns:
            str: encoding used for the resource
        """
        mimetype = mimetypes.guess_type(self.path)
        return mimetype[1]

    def get_content_length(self):
        """Get the length of the resource

        Returns:
            int: length of resource in bytes
        """
        with open(self.path) as content_file:
            content = content_file.read()
            content_file.close()
        return len(content)  # os.path.getsize(self.path)
