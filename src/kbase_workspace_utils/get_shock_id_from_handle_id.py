import json
import requests
from uuid import uuid4

from .load_config import load_config


def get_shock_id_from_handle_id(handle_id):
    config = load_config()
    request_data = {
        'method': 'AbstractHandle.hids_to_handles',
        'params': [[handle_id]],
        'id': str(uuid4())
    }
    resp = requests.post(config.handle_url, data=json.dumps(request_data))
    resp_json = resp.json()
    result = resp_json['result'][0][0]
    return result['id']
