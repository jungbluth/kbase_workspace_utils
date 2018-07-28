import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize some configuration data
auth_token = os.environ['KB_AUTH_TOKEN']
kbase_env = os.environ.get('KBASE_ENV', 'appdev').lower()
if kbase_env == 'prod':
    kbase_env == 'narrative'
ws_url = "https://" + kbase_env + ".kbase.us/services/ws"
shock_url = "https://" + kbase_env + ".kbase.us/services/shock-api"


def download_obj(*, ref):
    """
    Download a json object from the workspace.
    """
    method = 'Workspace.get_objects2'
    (ws_id, obj_id, obj_ver) = ref.split('/')
    params = [{'objects': [{'ref': ref}]}]
    data = {'method': method, 'params': params, 'version': 1.1}
    response = requests.post(
        ws_url,
        data=json.dumps(data),
        headers={'Authorization': auth_token},
        timeout=1800
    )
    resp_data = response.json()
    if 'error' in resp_data:
        raise ValueError(resp_data['error']['message'])
    ws_obj = resp_data['result'][0]
    # TODO deleted object error + test
    # TODO unauthorized access error + test
    if ws_obj.get('error'):
        raise ValueError(ws_obj['error']['message'])
    return ws_obj


def download_shock_file(shock_id, file_path):
    """
    Download a file from shock.
    Args:
      shock_id is the unique ID of a shock file object
    """
    headers = {'Authorization': 'OAuth ' + auth_token}
    node_url = shock_url + '/node/' + shock_id
    response = requests.get(node_url, headers=headers, allow_redirects=True)
    metadata = response.json()
    print('shock metadata', metadata)
    # First, we need to make a request to check for the existence of the file and get its name
    # metadata = download_shock_metadata(shock_id)
    # TODO error handling
    # if metadata['status'] == 401:
    #     return DownloadResult(error='Unauthorized', downloaded_file=None)
    # if metadata['status'] == 404:
    #     return DownloadResult(error='File not found', downloaded_file=None)
    # name = metadata['data']['file']['name']
    # Download the actual file
    response = requests.get(
        node_url + '?download_raw',
        headers=headers,
        allow_redirects=True,
        stream=True
    )
    with open(file_path, 'wb') as fwrite:
        for block in response.iter_content(1024):
            fwrite.write(block)


def download_assembly(*, ref, save_dir):
    """
    Download an Assembly object as fasta
    """
    # config = _get_config()
    obj = download_obj(ref=ref)['data'][0]
    # ws_type = obj['info'][2]
    obj_name = obj['info'][1]
    output_filename = obj_name + '.fa'
    output_path = os.path.join(save_dir, output_filename)
    shock_id = obj['data']['fasta_handle_info']['shock_id']
    download_shock_file(shock_id, output_path)
    return output_path


def download_reads(ref, **kwargs):
    return


def download_genome(ref, **kwargs):
    return
