import os
import functools
from collections import namedtuple
from dotenv import load_dotenv

load_dotenv()

Config = namedtuple('Config', ['auth_token', 'endpoint', 'ws_url', 'shock_url', 'handle_url'])


@functools.lru_cache()
def load_config():
    """
    Initialize some configuration data.
    This is memoized using functools
    """
    auth_token = os.environ.get('KB_AUTH_TOKEN')
    kbase_endpoint = os.environ.get('KBASE_ENDPOINT', 'https://appdev.kbase.us/services/')
    return Config(
        auth_token=auth_token,
        endpoint=kbase_endpoint,
        shock_url=kbase_endpoint + 'shock-api',
        ws_url=kbase_endpoint + 'ws',
        handle_url=kbase_endpoint + 'handle_service'
    )
