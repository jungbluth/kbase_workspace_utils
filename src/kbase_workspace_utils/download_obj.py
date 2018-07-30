"""
Download a workspace object.
"""

import json
import requests

from .load_config import load_config

config = load_config()


def download_obj(*, ref):
    """
    Download any object from the workspace.
    Keyword arguments:
      ref is a workspace reference ID in the form 'workspace_id/object_id/version'
    Returns the object as a dictionary of data
    """
    # Make the http request to the workspace service using JSON RPC 1.1
    # API spec: https://github.com/kbase/workspace_deluxe/blob/master/workspace.spec
    method = 'Workspace.get_objects2'
    params = [{'objects': [{'ref': ref}]}]
    data = {'method': method, 'params': params, 'version': 1.1}
    response = requests.post(
        config.ws_url,
        data=json.dumps(data),
        headers={'Authorization': config.auth_token},
        timeout=1800
    )
    resp_data = response.json()
    if 'error' in resp_data:
        raise ValueError(resp_data['error']['message'])
    ws_obj = resp_data['result'][0]
    # TODO deleted object error + test
    # TODO unauthorized access error + test
    return ws_obj


class MissingWSObject(Exception):
    pass  # TODO


class UnauthorizedWSAccess(Exception):
    pass  # TODO
