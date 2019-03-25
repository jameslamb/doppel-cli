
from functools import lru_cache


@lru_cache(maxsize=1)
def function_c(**kwargs):
    pass
