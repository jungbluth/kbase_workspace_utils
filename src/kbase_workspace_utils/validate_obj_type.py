"""
Validate the types of workspace objects.

For example, calling download_reads should only work on Reads types.
"""


def validate_obj_type(ws_obj, types):
    """
    Given a workspace object, validate that its types match any of the strings in `types`

    raises an InvalidWSType error
    """
    ws_type = ws_obj['info'][2]
    if all(t not in ws_type for t in types):
        raise InvalidWSType(given=ws_type, valid=types)


class InvalidWSType(Exception):

    def __init__(self, given, valid):
        self.given = given
        self.valid = valid

    def __str__(self):
        return "Invalid workspace type: " + self.given + ". Valid types are: " + str(self.valid)
