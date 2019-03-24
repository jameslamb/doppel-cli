
class ClassC:

    def __init__(self, **kwargs):
        pass

    @classmethod
    def from_string(cls, the_string):
        return(cls(the_string=the_string))
