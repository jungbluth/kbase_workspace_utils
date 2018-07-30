import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# TODO error handling and exception classes

# Initialize some configuration data
auth_token = os.environ['KB_AUTH_TOKEN']
kbase_env = os.environ.get('KBASE_ENV', 'appdev').lower()
if kbase_env == 'prod':
    kbase_env == 'narrative'
ws_url = "https://" + kbase_env + ".kbase.us/services/ws"
shock_url = "https://" + kbase_env + ".kbase.us/services/shock-api"


def download_obj(*, ref):
    """
    Download any object from the workspace.
    Keyword arguments:
      ref is a workspace reference ID in the form 'workspace_id/object_id/version'
    Returns the object as a dictionary of data
    """
    method = 'Workspace.get_objects2'
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
    return ws_obj


def download_shock_file(shock_id, file_path):
    """
    Download a file from shock.
    Keyword arguments:
      shock_id is the unique ID of a shock file object
    Returns nothing
    """
    # TODO error handling and classes
    if os.path.exists(file_path):
        raise ValueError('File already exists at ' + file_path)
    headers = {'Authorization': 'OAuth ' + auth_token}
    node_url = shock_url + '/node/' + shock_id
    response = requests.get(node_url, headers=headers, allow_redirects=True)
    # metadata = response.json()
    # First, we need to make a request to check for the existence of the file and get its name
    # metadata = download_shock_metadata(shock_id)
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
    Download an Assembly object as fasta.
    Keyword arguments:
      ref is a workspace reference ID in the form 'workspace_id/object_id/version'
      save_dir is the path of a directory in which to save the fasta file
    """
    # TODO error handling and classes
    ws_obj = download_obj(ref=ref)['data'][0]
    # ws_type = obj['info'][2]
    # # catch the wrong type here
    obj_name = ws_obj['info'][1]
    output_filename = obj_name + '.fasta'
    output_path = os.path.join(save_dir, output_filename)
    if os.path.exists(output_path):
        raise ValueError('File already exists at ' + output_path)
    shock_id = ws_obj['data']['fasta_handle_info']['shock_id']
    download_shock_file(shock_id, output_path)
    return output_path


def download_reads(*, ref, save_dir):
    """
    Download genome reads data as fastq.
    Keyword arguments:
      ref is a workspace reference ID in the form 'workspace_id/object_id/version'
      save_dir is the path of a directory in which to save the fasta file
    Returns a list of paths of the downloaded fastq files.

    If the reads are paired-end and non-interleaved, you will get two files, one for the forward
    (left) reads and one for the reverse (right) reads. Otherwise, you will get one file.

    File-names:
    - Paired ends and interleaved get the file ending of '.paired.interleaved.fastq'
    - Paired ends and non-interleaved get the file ending of '.paired.fwd.fastq' and
        '.paired.rev.fastq'
    - Single ends get the file ending of '.single.fastq'
    """
    # TODO error handling and classes
    ws_obj = download_obj(ref=ref)['data'][0]
    obj_name = ws_obj['info'][1]
    ws_type = ws_obj['info'][2]
    if 'SingleEnd' in ws_type:
        shock_ids = [ws_obj['data']['lib']['file']['id']]
        output_paths = [os.path.join(save_dir, obj_name + '.single.fastq')]
    elif 'PairedEnd' in ws_type:
        interleaved = ws_obj['data']['interleaved']
        if interleaved:
            shock_ids = [ws_obj['data']['lib1']['file']['id']]
            output_paths = [os.path.join(save_dir, obj_name + '.paired.interleaved.fastq')]
        else:
            shock_ids = [
                ws_obj['data']['lib1']['file']['id'],
                ws_obj['data']['lib2']['file']['id']
            ]
            output_paths = [
                os.path.join(save_dir, obj_name + '.paired.fwd.fastq'),
                os.path.join(save_dir, obj_name + '.paired.rev.fastq')
            ]
    else:
        raise ValueError('This workspace object contains neither a ' +
                         'paired-end nor a single-end reads dataset')
    for (path, sid) in zip(output_paths, shock_ids):
        download_shock_file(sid, path)
    return output_paths


def download_genome(ref, **kwargs):
    return
