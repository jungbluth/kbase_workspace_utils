import requests
import os

from .load_config import load_config
from .exceptions import FileExists


def download_shock_file(shock_id, file_path, auth_token=None):
    """
    Download a file from shock.
    Keyword arguments:
      shock_id is the unique ID of a shock file object
      file_path is a valid, non-existent path where the file will get downloaded
    Returns nothing
    """
    config = load_config()
    auth_token = auth_token or config.auth_token
    if os.path.exists(file_path):
        raise FileExists('File already exists at ' + file_path)
    headers = {'Authorization': 'OAuth ' + config.auth_token}
    # First we need to fetch some metadata about the file from shock
    node_url = config.shock_url + '/node/' + shock_id
    response = requests.get(node_url, headers=headers, allow_redirects=True)
    metadata = response.json()
    # Make sure the shock file is present and valid
    if metadata['status'] == 401:
        raise UnauthorizedShockDownload(shock_id)
    if metadata['status'] == 404:
        raise MissingShockFile(shock_id)
    # Now that everything looks okay, we fetch the actual file
    response = requests.get(
        node_url + '?download_raw',
        headers=headers,
        allow_redirects=True,
        stream=True
    )
    with open(file_path, 'wb') as fwrite:
        for block in response.iter_content(1024):
            fwrite.write(block)


class UnauthorizedShockDownload(Exception):
    """The user does not have access to this shock file."""

    def __init__(self, id_):
        self.id = id_

    def __str__(self):
        return "Unauthorized access to shock file with ID " + self.id


class MissingShockFile(Exception):
    """There is no shock file for the given shock ID."""

    def __init__(self, id_):
        self.id = id_

    def __str__(self):
        return "Missing shock file with ID " + self.id
