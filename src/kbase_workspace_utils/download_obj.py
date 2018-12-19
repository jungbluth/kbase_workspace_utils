"""
Download a workspace object.
"""
import json
import requests

from .load_config import load_config
from .exceptions import InvalidUser, InaccessibleWSObject, InvalidWSResponse


def download_obj(ref, auth_token=None):
    """
    Download any object from the workspace.
    Keyword arguments:
      ref is a workspace reference ID in the form 'workspace_id/object_id/version'
    Returns the object as a dictionary of data
    """
    # Make the http request to the workspace service using JSON RPC 1.1
    # API spec: https://github.com/kbase/workspace_deluxe/blob/master/workspace.spec
    config = load_config()
    method = 'Workspace.get_objects2'
    params = [{'objects': [{'ref': ref}]}]
    data = {'method': method, 'params': params, 'version': 1.1}
    auth_token = auth_token or config.auth_token
    headers = {}
    if auth_token:
        headers['Authorization'] = auth_token
    response = requests.post(
        config.ws_url,
        data=json.dumps(data),
        headers=headers
    )
    try:
        json_data = response.json()
    except ValueError as err:
        print(err)
        raise InvalidWSResponse("JSON parsing error: " + response.text)
    return _handle_response(json_data, config)


def _handle_response(resp_data, config):
    """Handle the JSON object return by a workspace response when fetching an object."""
    if 'error' in resp_data:
        code = resp_data['error']['code']
        if code == -32400:
            raise InvalidUser(resp_data['error']['message'] + '. KBase endpoint is ' + config.endpoint)
        if code == -32500:
            raise InaccessibleWSObject(resp_data['error']['message'])
        else:
            raise ValueError(resp_data['error']['message'])
    ws_obj = resp_data['result'][0]
    return ws_obj
