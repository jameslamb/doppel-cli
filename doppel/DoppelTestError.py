
class DoppelTestError:

    def __init__(self, msg: str):
        """
        Custom error class used for testing issues.

        :param msg: Error text to print
        """
        self.msg = msg

    def __str__(self):
        return("{}\n".format(self.msg))
