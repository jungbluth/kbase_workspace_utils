import os

from .contigset_to_fasta import contigset_to_fasta
from .download_obj import download_obj
from .download_shock_file import download_shock_file
from .exceptions import FileExists
from .validate_obj_type import validate_obj_type
from .get_shock_id_from_handle_id import get_shock_id_from_handle_id


def download_assembly(ref, save_dir, auth_token=None):
    """
    Download an Assembly object as fasta.
    Keyword arguments:
      ref is a workspace reference ID in the form 'workspace_id/object_id/version'
      save_dir is the path of a directory in which to save the fasta file
    Returns an absolute path of the downloaded fasta file.
    """
    ws_obj = download_obj(ref, auth_token=auth_token)['data'][0]
    valid_types = ['KBaseGenomeAnnotations.Assembly', 'ContigSet']
    validate_obj_type(ws_obj=ws_obj, types=valid_types)
    (obj_name, obj_type) = (ws_obj['info'][1], ws_obj['info'][2])
    output_path = os.path.abspath(os.path.join(save_dir, obj_name + '.fasta'))
    if os.path.exists(output_path):
        raise FileExists('File already exists at ' + output_path)
    if 'ContigSet' in obj_type:
        # Write out ContigSet data into a fasta file
        contigset_to_fasta(ws_obj, output_path)
    else:
        # Download a linked fasta file to the save directory
        data = ws_obj['data']
        if 'fasta_handle_info' in data and 'shock_id' in data['fasta_handle_info']:
            shock_id = data['fasta_handle_info']['shock_id']
        else:
            handle_id = data['fasta_handle_ref']
            shock_id = get_shock_id_from_handle_id(handle_id)
        download_shock_file(shock_id, output_path, auth_token=auth_token)
    return output_path
