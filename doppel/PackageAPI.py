import json
from typing import Dict
from typing import List


def _log_info(msg):
    print(msg)


CLASSES_KEY: str = "classes"
FUNCTIONS_KEY: str = "functions"


class PackageAPI():
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

    @classmethod
    def from_json(cls, filename: str, ignore_classes: bool, ignore_functions: bool):
        """
        Instantiate a Package object from a JSON file.

        :param filename: Name of the JSON file
            that contains the description of the
            target package's API.
        :param ignore_classes: Ignore classes in
            package comparisons. See docs in ``cli.py``
            for more information.
        :param ignore_functions: Ignore functions in
            package comparisons. See docs in ``cli.py``
            for more information.
        """
        _log_info("Creating package from {}".format(filename))

        # read in output of "analyze.*" script
        with open(filename, 'r') as f:
            pkg_dict = json.loads(f.read())

        if ignore_classes:
            pkg_dict[CLASSES_KEY] = {}

        if ignore_functions:
            pkg_dict[FUNCTIONS_KEY] = {}

        # validate
        return cls(pkg_dict)

    def _validate_pkg(self, pkg_dict: dict) -> None:

        assert isinstance(pkg_dict, dict)
        assert pkg_dict['name'] is not None
        assert pkg_dict['language'] is not None
        assert pkg_dict[FUNCTIONS_KEY] is not None
        assert pkg_dict[CLASSES_KEY] is not None

        return

    def name(self) -> str:
        """
        Get the name of the package.
        """
        return(self.pkg_dict['name'])

    def num_functions(self) -> int:
        """
        Get the number of exported functions in the package.
        """
        return(len(self.function_names()))

    def function_names(self) -> List[str]:
        """
        Get a list with the names of all exported functions
        in the package.
        """
        return(sorted(list(self.pkg_dict[FUNCTIONS_KEY].keys())))

    def functions_with_args(self) -> Dict[str, Dict]:
        """
        Get a dictionary with all exported functions in the package
        and some  details describing them.
        """
        return(self.pkg_dict[FUNCTIONS_KEY])

    def num_classes(self) -> int:
        """
        Get the number of exported classes in the package.
        """
        return(len(self.class_names()))

    def class_names(self) -> List[str]:
        """
        Get a list with the names of all exported classes
        in the package.
        """
        return(sorted(list(self.pkg_dict[CLASSES_KEY].keys())))

    def public_methods(self, class_name: str) -> List[str]:
        """
        Get a list with the names of all public methods for a class.

        :param class_name: Name of a class in the package
        """
        return(sorted(list(self.pkg_dict[CLASSES_KEY][class_name]['public_methods'].keys())))

    def public_method_args(self, class_name: str, method_name: str) -> List[str]:
        """
        Get a list of arguments for a public method from a class.

        :param class_name: Name of a class in the package
        :param method-name: Name of the method to get arguments for
        """
        return(list(self.pkg_dict[CLASSES_KEY][class_name]['public_methods'][method_name]['args']))
