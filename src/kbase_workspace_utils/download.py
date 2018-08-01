import os
from Bio import SeqIO

from .load_config import load_config
from .contigset_to_fasta import contigset_to_fasta
from .download_shock_file import download_shock_file
from .download_obj import download_obj
from .validate_obj_type import validate_obj_type
from .exceptions import InvalidWSType, FileExists

config = load_config()


def download_assembly(ref, save_dir):
    """
    Download an Assembly object as fasta.
    Keyword arguments:
      ref is a workspace reference ID in the form 'workspace_id/object_id/version'
      save_dir is the path of a directory in which to save the fasta file
    """
    ws_obj = download_obj(ref=ref)['data'][0]
    validate_obj_type(ws_obj, types=['Assembly', 'ContigSet'])
    (obj_name, obj_type) = (ws_obj['info'][1], ws_obj['info'][2])
    output_path = os.path.join(save_dir, obj_name + '.fasta')
    if os.path.exists(output_path):
        raise FileExists('File already exists at ' + output_path)
    # TODO handle the full type name here
    if 'ContigSet' in obj_type:
        # Write out ContigSet data into a fasta file
        SeqIO.write(contigset_to_fasta(ws_obj), output_path, "fasta")
    else:
        # Download a linked fasta file to the save directory
        shock_id = ws_obj['data']['fasta_handle_info']['shock_id']
        download_shock_file(shock_id, output_path)
    return output_path


def download_reads(ref, save_dir):
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
    ws_obj = download_obj(ref=ref)['data'][0]
    (obj_name, obj_type) = (ws_obj['info'][1], ws_obj['info'][2])
    # TODO use the full type names
    if 'SingleEnd' in obj_type:
        # One file to download
        shock_id = ws_obj['data']['lib']['file']['id']
        path = os.path.join(save_dir, obj_name + '.single.fastq')
        to_download = [(shock_id, path)]
    elif 'PairedEnd' in obj_type:
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
        raise InvalidWSType(given=obj_type, valid=['SingleEnd', 'PairedEnd'])
    # Download each shock id to each path
    for (shock_id, path) in to_download:
        download_shock_file(shock_id, path)
    output_paths = map(lambda pair: pair[1], to_download)
    return list(output_paths)


def get_assembly_from_genome(ref):
    """
    Given a Genome object, fetch the reference to its Assembly object on the workspace.
    Arguments:
      ref is a workspace reference ID in the form 'workspace_id/object_id/version'
    Returns a workspace reference to an assembly object
    """
    # Fetch the workspace object and check its type
    ws_obj = download_obj(ref=ref)['data'][0]
    validate_obj_type(ws_obj, ['Genome'])
    # Extract out the assembly reference from the workspace data
    ws_data = ws_obj['data']
    assembly_ref = ws_data.get('contigset_ref') or ws_data.get('assembly_ref')
    if not assembly_ref:
        raise ValueError('Genome ' + ref + ' has no assembly or contigset references')
    # Return a reference path of `genome_ref;assembly_ref`
    ref_path = ref + ';' + assembly_ref
    return ref_path


def download_genome(ref, save_dir):
    raise NotImplementedError()
    # ws_obj = download_obj(ref=ref)['data'][0]
    # obj_name = ws_obj['info'][1]
    # ws_type = ws_obj['info'][2]
    # filename = obj_name + '.gbff'
    # output_path = os.path.join(save_dir, filename)
    # # genbank file is gbff
    # if 'Genome' not in ws_type:
    #     raise ValueError('Invalid type for a Genome download: ' + ws_type)
    # return (output_path)
