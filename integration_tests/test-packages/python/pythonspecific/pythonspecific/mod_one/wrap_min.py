
# used to test the "cannot get signature of builtin" code
wrap_min = min


class MinWrapper:
    def __init__(self):
        pass
    wrap_min = min
