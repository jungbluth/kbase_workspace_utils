import os
import shutil
import tempfile
import unittest

from dotenv import load_dotenv
load_dotenv()  # noqa

from src.kbase_workspace_utils import download_reads
from src.kbase_workspace_utils.exceptions import InvalidWSType


class TestDownloadReads(unittest.TestCase):

    def test_basic_valid(self):
        """
        Test valid downloads for both paired and single-end reads. Paired-end has examples for both
        interleaved and not.
        """
        tmp_dir = tempfile.mkdtemp()
        # Paired reads, non-interleaved
        ref = '15/45/1'
        paths = download_reads(ref=ref, save_dir=tmp_dir)
        self.assertEqual(len(paths), 2)
        self.assertTrue('rhodobacter.art.q10.PE.reads.paired.fwd.fastq' in paths[0])
        self.assertTrue('rhodobacter.art.q10.PE.reads.paired.rev.fastq' in paths[1])
        self.assertEqual(os.path.getsize(paths[0]), 36056522)
        self.assertEqual(os.path.getsize(paths[1]), 37522557)
        # Paired reads, interleaved
        ref = '15/44/1'
        paths = download_reads(ref=ref, save_dir=tmp_dir)
        self.assertTrue('rhodobacter.art.q20.int.PE.reads.paired.interleaved.fastq' in paths[0])
        self.assertEqual(len(paths), 1)
        self.assertEqual(os.path.getsize(paths[0]), 36510129)
        # Single-end reads
        ref = '15/43/1'
        paths = download_reads(ref=ref, save_dir=tmp_dir)
        self.assertTrue('rhodobacter.art.q50.SE.reads.single.fastq' in paths[0])
        self.assertEqual(len(paths), 1)
        self.assertEqual(os.path.getsize(paths[0]), 53949468)
        shutil.rmtree(tmp_dir)

    # Error cases for invalid users and invalid ws references are covered in test_download_obj

    def test_download_wrong_type(self):
        assembly_id = '34819/10/1'
        tmp_dir = tempfile.mkdtemp()
        with self.assertRaises(InvalidWSType) as err:
            download_reads(ref=assembly_id, save_dir=tmp_dir)
        self.assertTrue('Invalid workspace type' in str(err.exception))
        shutil.rmtree(tmp_dir)
