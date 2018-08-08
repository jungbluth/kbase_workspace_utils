"""
Validate the types of workspace objects.

For example, calling download_reads should only work on Reads types.
"""
from .exceptions import InvalidWSType


def validate_obj_type(ws_obj, types):
    """
    Given a workspace object, validate that its types match any of the strings in `types`.
    Args:
      ws_obj is a workspace reference in the form of 'workspace_id/object_id/version'
      types is a list of string type names to match against
    raises an InvalidWSType error
    returns None
    """
    ws_type = ws_obj['info'][2]
    if all(t not in ws_type for t in types):
        raise InvalidWSType(given=ws_type, valid_types=types)
