from warnings import warn
from requests import get  # noqa
from requests import post as custom_post  # noqa


def create_warning():
    print("uh oh")
    warn("not good")


shmeate_schmarning = warn


def create_warm_things(**kwargs):
    warn(**kwargs)


def _super_secret():
    print("shhhh")
