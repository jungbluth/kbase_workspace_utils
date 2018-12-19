import unittest

from dotenv import load_dotenv
load_dotenv()  # noqa

from src.kbase_workspace_utils import get_assembly_from_genome
from src.kbase_workspace_utils.exceptions import InvalidGenome


class TestGetAssemblyFromGenome(unittest.TestCase):

    def test_basic_valid(self):
        """Test the valid/successful case."""
        ref = '34819/14/1'
        assembly_ref = get_assembly_from_genome(ref)
        self.assertEqual(assembly_ref, '34819/14/1;16/7/1')

    def test_does_not_have_assembly(self):
        """
        Test the case where a Genome object does not have an assembly_ref
        """
        ref = '34819/5/9'
        with self.assertRaises(InvalidGenome) as err:
            get_assembly_from_genome(ref)
        self.assertTrue('no assembly or contigset references' in str(err.exception))
