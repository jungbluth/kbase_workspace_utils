import os
import unittest
from src.kbase_workspace_utils import download_obj
from src.kbase_workspace_utils.exceptions import InvalidUser, InaccessibleWSObject


class TestDownloadObj(unittest.TestCase):

    def test_basic_valid(self):
        """Test a basic valid download."""
        valid_ws_id = '15/38/4'  # TODO need static, public example data
        obj = download_obj(ref=valid_ws_id)
        self.assertEqual(obj['data'][0]['created'], '2015-02-06T20:51:01+0000')

    def test_nonexistent_ref(self):
        """Test a download where the ref is non-existent."""
        invalid_ws_id = '6666666666/1/1'
        with self.assertRaises(InaccessibleWSObject) as err:
            download_obj(ref=invalid_ws_id)
        self.assertTrue('cannot be accessed' in str(err.exception))

    def test_unauthorized_ref(self):
        """Test a download where the ref is unauthorized."""
        invalid_ws_id = '1/1/1'
        with self.assertRaises(InaccessibleWSObject) as err:
            download_obj(ref=invalid_ws_id)
            self.assertTrue('cannot be accessed' in str(err.exception))

    def test_unauthorized_user(self):
        invalid_ws_id = '1/1/1'
        prev_token = os.environ['KB_AUTH_TOKEN']
        os.environ['KB_AUTH_TOKEN'] = 'xxx'
        with self.assertRaises(InvalidUser) as err:
            download_obj(ref=invalid_ws_id)
        self.assertTrue('Login failed' in str(err.exception))
        os.environ['KB_AUTH_TOKEN'] = prev_token

    # TODO test all error cases
