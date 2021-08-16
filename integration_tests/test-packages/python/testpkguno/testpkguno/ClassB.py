from .ClassA import ClassA


class ClassB(ClassA):
    def __init__(self, **kwargs):
        pass

    # Overwriting one method from ClassA to
    # test that ordering of inheritance is
    # respected
    def banarchy(self, nonsense=True):
        return nonsense

    def hello_there(self, greeting):
        pass


# Adding an internal class to be sure tests catch
# these suddenly getting picked up by analyze.py
class _SomeInternalClass:
    def __init__(self, x):
        self.x = x
