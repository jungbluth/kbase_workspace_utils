import os
import shutil
import tempfile
import unittest
from src.kbase_workspace_utils import download_assembly


class TestDownloadAssembly(unittest.TestCase):

    def test_basic_valid(self):
        tmp_dir = tempfile.mkdtemp()
        valid_ws_id = '34819/10/1'
        pathname = download_assembly(ref=valid_ws_id, save_dir=tmp_dir)
        self.assertEqual(os.path.getsize(pathname), 3849120)
        filename = os.path.basename(pathname)
        self.assertEqual(filename, "MEGAHIT.contigs.fasta")
        shutil.rmtree(tmp_dir)

    # TODO test contigset download

    # TODO Test all error cases
