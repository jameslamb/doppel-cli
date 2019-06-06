from functools import lru_cache


class ClassA:

    story1 = True
    story3 = "hello"
    _secret1 = True

    def __init__(self, x, y, *, z):
        pass

    def anarchy(**kwargs):
        pass

    def banarchy(self, thing_1, thing_2, yes):
        pass

    @lru_cache(maxsize=1)
    def canarchy(self, x, y, **kwargs):
        pass

    def _acclimate(self, **kwargs):
        pass

    def _caclimate(self):
        pass
