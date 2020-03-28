
class DoppelTestError:

    def __init__(self, msg: str) -> None:
        """
        Custom error class used for testing issues.

        :param msg: Error text to print
        """
        self.msg = msg

    def __str__(self) -> str:
        return("{}\n".format(self.msg))
