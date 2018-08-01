"""
Error classes used in this package.
"""


class InvalidUser(Exception):
    """Invalid token for user; cannot authenticate."""
    pass


class InaccessibleWSObject(Exception):
    """A workspace object is inaccessible to the user."""
    pass
