"""
Error classes used in this package.
"""


class InvalidUser(Exception):
    """Invalid token for user; cannot authenticate."""
    pass


class InaccessibleWSObject(Exception):
    """A workspace object is inaccessible to the user."""
    pass


class InvalidWSType(Exception):

    def __init__(self, given, valid_types):
        self.given = given
        self.valid_types = valid_types

    def __str__(self):
        types = ", ".join(self.valid_types)
        return "Invalid workspace type: " + self.given + ". Valid types are: " + types


class FileExists(Exception):
    """A file already exists at a path where we want to download something."""
    pass


class InvalidGenome(Exception):
    """The genome object does not have the right data structure for download."""
    pass


class InvalidWSResponse(Exception):

    def __init__(self, response_text):
        self.resp = response_text

    def __str__(self):
        return "Invalid response from the workspace:\n%s" % self.resp
