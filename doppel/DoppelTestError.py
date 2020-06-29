"""
Custom error class for testing errors
"""


class DoppelTestError:
    """
    Custom error class used for testing issues.

    :param msg: Error text to print
    """

    def __init__(self, msg: str) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return "{}\n".format(self.msg)
