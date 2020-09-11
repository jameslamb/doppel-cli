"""
Class for package details.
"""

import json

from copy import deepcopy
from typing import Dict
from typing import List

CLASSES_KEY = "classes"
FUNCTION_KEY = "functions"
PUBLIC_METHODS_KEY = "public_methods"


def _log_info(msg):
    print(msg)


def _uncase_all_keys(in_dict: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Given a dictionary, replace all of its keys except
    special doppel ones with "uncased" values:

    * lowercase
    * remove ``_``, ``.``
    """
    special_keys = set([
        "args",
        CLASSES_KEY,
        FUNCTION_KEY,
        PUBLIC_METHODS_KEY
    ])
    new_dict = {}
    out_dict = deepcopy(in_dict)
    for k, v in out_dict:
        new_key = k.lower().replace(".", "").replace("_", "")
        if isinstance(v, dict):
            new_dict[new_key] = _uncase_all_keys(v)
        else:
            new_dict[new_key] = v
    return new_dict


class PackageAPI:
    """Package API class

    This class is used to hold the interface of a given package
    being analyzed by doppel. It's comparison operators enable comparison
    between interfaces and its standard JSON format allows this comparison
    to happen across programming languages.

    """

    def __init__(self, pkg_dict: dict):
        """
        Class containing data that describes a package API

        :param pkg_dict: A dictionary representation of a
            software package, complying with the output format of
            doppel-describe.

        """

        self._validate_pkg(pkg_dict)
        self.pkg_dict = pkg_dict

    def remove_casing(self) -> None:
        """
        This method removes all casing information from
        a package.

        Raises a ``RuntimeError`` if removing casing would
        cause problems.
        """
        self.pkg_dict = _uncase_all_keys(self.pkg_dict)

    @classmethod
    def from_json(cls, filename: str) -> "PackageAPI":
        """
        Instantiate a Package object from a file.

        :param filename: Name of the JSON file
            that contains the description of the
            target package's API.

        """
        _log_info("Creating package from {}".format(filename))

        # read in output of "analyze.*" script
        with open(filename, "r") as f:
            pkg_dict = json.loads(f.read())

        # validate
        return cls(pkg_dict)

    @staticmethod
    def _validate_pkg(pkg_dict: dict) -> None:

        assert isinstance(pkg_dict, dict)
        assert pkg_dict["name"] is not None
        assert pkg_dict["language"] is not None
        assert pkg_dict[FUNCTION_KEY] is not None
        assert pkg_dict[CLASSES_KEY] is not None

    def name(self) -> str:
        """
        Get the name of the package.
        """
        return self.pkg_dict["name"]

    def num_functions(self) -> int:
        """
        Get the number of exported functions in the package.
        """
        return len(self.function_names())

    def function_names(self) -> List[str]:
        """
        Get a list with the names of all exported functions
        in the package.
        """
        return sorted(list(self.pkg_dict[FUNCTION_KEY].keys()))

    def functions_with_args(self) -> Dict[str, Dict]:
        """
        Get a dictionary with all exported functions in the package
        and some  details describing them.
        """
        return self.pkg_dict[FUNCTION_KEY]

    def num_classes(self) -> int:
        """
        Get the number of exported classes in the package.
        """
        return len(self.class_names())

    def class_names(self) -> List[str]:
        """
        Get a list with the names of all exported classes
        in the package.
        """
        return sorted(list(self.pkg_dict[CLASSES_KEY].keys()))

    def public_methods(self, class_name: str) -> List[str]:
        """
        Get a list with the names of all public methods for a class.

        :param class_name: Name of a class in the package
        """
        return sorted(list(self.pkg_dict[CLASSES_KEY][class_name][PUBLIC_METHODS_KEY].keys()))

    def public_method_args(self, class_name: str, method_name: str) -> List[str]:
        """
        Get a list of arguments for a public method from a class.

        :param class_name: Name of a class in the package
        :param method-name: Name of the method to get arguments for
        """
        return list(self.pkg_dict[CLASSES_KEY][class_name][PUBLIC_METHODS_KEY][method_name]["args"])
