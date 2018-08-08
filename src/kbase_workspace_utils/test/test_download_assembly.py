import os
import shutil
import tempfile
import unittest
from src.kbase_workspace_utils.exceptions import InvalidWSType
from src.kbase_workspace_utils import download_assembly


class TestDownloadAssembly(unittest.TestCase):

    def test_basic_valid(self):
        tmp_dir = tempfile.mkdtemp()
        valid_ws_id = '34819/10/1'
        pathname = download_assembly(valid_ws_id, tmp_dir, auth_token=os.environ['KB_AUTH_TOKEN'])
        self.assertEqual(os.path.getsize(pathname), 3849120)
        filename = os.path.basename(pathname)
        self.assertEqual(filename, "MEGAHIT.contigs.fasta")
        shutil.rmtree(tmp_dir)

    # Error cases for invalid users and invalid ws references are covered in test_download_obj

    def test_download_wrong_type(self):
        reads_id = '15/45/1'
        tmp_dir = tempfile.mkdtemp()
        with self.assertRaises(InvalidWSType) as err:
            download_assembly(ref=reads_id, save_dir=tmp_dir)
        self.assertTrue('Invalid workspace type' in str(err.exception))
        shutil.rmtree(tmp_dir)

    # TODO test contigset download

    # TODO Test more error cases
