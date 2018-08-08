import os

from .download_obj import download_obj
from .download_shock_file import download_shock_file
from .exceptions import InvalidWSType


def download_reads(ref, save_dir, auth_token=None):
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
    # Fetch the workspace object and check its type
    ws_obj = download_obj(ref, auth_token=auth_token)['data'][0]
    (obj_name, obj_type) = (ws_obj['info'][1], ws_obj['info'][2])
    valid_types = {
        'single': 'SingleEndLibrary-2.0',
        'paired': 'PairedEndLibrary-2.0'
    }
    if valid_types['single'] in obj_type:
        # One file to download
        shock_id = ws_obj['data']['lib']['file']['id']
        path = os.path.join(save_dir, obj_name + '.single.fastq')
        to_download = [(shock_id, path)]
    elif valid_types['paired'] in obj_type:
        interleaved = ws_obj['data']['interleaved']
        if interleaved:
            # One file to download
            shock_id = ws_obj['data']['lib1']['file']['id']
            path = os.path.join(save_dir, obj_name + '.paired.interleaved.fastq')
            to_download = [(shock_id, path)]
        else:
            # Two files to download (for left and right reads)
            shock_id_fwd = ws_obj['data']['lib1']['file']['id']
            shock_id_rev = ws_obj['data']['lib2']['file']['id']
            path_fwd = os.path.join(save_dir, obj_name + '.paired.fwd.fastq')
            path_rev = os.path.join(save_dir, obj_name + '.paired.rev.fastq')
            to_download = [(shock_id_fwd, path_fwd), (shock_id_rev, path_rev)]
    else:
        # Unrecognized type
        raise InvalidWSType(given=obj_type, valid_types=valid_types.values())
    # Download each shock id to each path
    for (shock_id, path) in to_download:
        download_shock_file(shock_id, path)
    # Return a list of the output paths that we have downloaded
    output_paths = map(lambda pair: pair[1], to_download)
    return list(output_paths)
