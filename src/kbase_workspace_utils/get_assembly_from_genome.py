
from .download_obj import download_obj
from .validate_obj_type import validate_obj_type
from .exceptions import InvalidGenome


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
        raise InvalidGenome('Genome ' + ref + ' has no assembly or contigset references')
    # Return a reference path of `genome_ref;assembly_ref`
    ref_path = ref + ';' + assembly_ref
    return ref_path
