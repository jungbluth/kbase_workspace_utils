import os
import functools
from collections import namedtuple
from dotenv import load_dotenv

load_dotenv()

Config = namedtuple('Config', ['auth_token', 'env', 'ws_url', 'shock_url', 'handle_url'])


@functools.lru_cache()
def load_config():
    """
    Initialize some configuration data.
    This is memoized using functools
    """
    auth_token = os.environ.get('KB_AUTH_TOKEN')
    kbase_env = os.environ.get('KBASE_ENV', 'appdev').lower()
    if kbase_env == 'prod' or kbase_env == 'production':
        kbase_env = 'narrative'
    return Config(
        auth_token=auth_token,
        env=kbase_env,
        shock_url="https://" + kbase_env + ".kbase.us/services/shock-api",
        ws_url="https://" + kbase_env + ".kbase.us/services/ws",
        handle_url="https://" + kbase_env + ".kbase.us/services/handle_service"
    )
