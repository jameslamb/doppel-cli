import unittest
from doppel.cli import _log_info


class TestStuff(unittest.TestCase):

    def test_logging(self):
        """
        _log_info should work
        """
        _log_info('stuff')
        self.assertTrue(True)
