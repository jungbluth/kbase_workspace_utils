# import os
# import shutil
import unittest
from src.kbase_workspace_utils import download_obj


class TestDownloadObj(unittest.TestCase):

    def test_basic_valid(self):
        """Test a basic valid download."""
        valid_ws_id = '15/38/4'  # TODO need static, public example data
        obj = download_obj(ref=valid_ws_id)
        self.assertEqual(obj['data'][0]['created'], '2015-02-06T20:51:01+0000')

    def test_unauthorized(self):
        """Test a download where the workspace is unauthorized."""
        invalid_ws_id = '1/1/1'
        with self.assertRaises(ValueError) as err:
            download_obj(ref=invalid_ws_id)
        self.assertTrue('cannot be accessed' in str(err.exception))
