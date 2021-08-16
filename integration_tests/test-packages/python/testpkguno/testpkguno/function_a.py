# Adding these imports to be sure that analyze.py
# isn't tricked into thinking they belong to this
# package
import math
from random import LOG4  # type: ignore


# Adding an internal function to be sure tests catch
# these suddenly getting picked up by analyze.py
def _add_5(n):
    return n + 5


def function_a():
    return math.pi + _add_5(LOG4)
