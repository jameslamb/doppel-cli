import unittest
import os
from doppel import DoppelTestError


class TestDoppelTestError(unittest.TestCase):
    """
    DoppelTestError should work
    """

    def test_basic(self):
        e = DoppelTestError("hello I am a message")
        self.assertEqual(
            e.msg,
            "hello I am a message"
        )

        txt = str(e)
        self.assertEqual(
            txt,
            "hello I am a message\n"
        )
