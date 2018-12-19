import shutil
import tempfile
import unittest

from dotenv import load_dotenv
load_dotenv()  # noqa

from src.kbase_workspace_utils import download_genome


class TestDownloadGenome(unittest.TestCase):

    @unittest.skip('TODO')
    def test_basic_valid(self):
        refs = [
            # '34819/14/1',
            # '34819/13/1',
            # '34819/3/2',
            # '34819/12/8',
            '34819/5/9'
        ]
        tmp_dir = tempfile.mkdtemp()
        for ref in refs:
            pathname = download_genome(ref=ref, save_dir=tmp_dir)
            print('*' * 100)
            print('ref', ref)
            print(pathname)
            print('*' * 100)
        shutil.rmtree(tmp_dir)

    # Test all error cases
