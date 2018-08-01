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

    def __init__(self, given, valid):
        self.given = given
        self.valid = valid

    def __str__(self):
        return "Invalid workspace type: " + self.given + ". Valid types are: " + str(self.valid)


class FileExists(Exception):
    """A file already exists at a path where we want to download something."""
    pass
