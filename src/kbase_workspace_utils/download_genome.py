

def download_genome(ref, save_dir, auth_token=None):
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
