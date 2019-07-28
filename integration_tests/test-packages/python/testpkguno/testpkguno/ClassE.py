
class ClassE:

    def __init__(self):
        """
        This is ClassE, a class whose constructor has
        no keyword arguments and which has a class
        method with no keyword args
        """
        pass

    @classmethod
    def from_string(cls):
        return(cls())
