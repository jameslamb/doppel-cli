import json


def _log_info(msg):
    print(msg)


class PackageAPI():
    """Package API class

    This class is used to hold the interface of a given package
    being analyzed by doppel. It's comparison operators enable comparison
    between interfaces and its standard JSON format allows this comparison
    to happen across programming languages.

    """

    def __init__(self, pkg_dict: dict):
        """Python object containing data that describes a package API

        :param pkg_dict: A dictionary representation of a
            software package, complying with the output format of
            doppel-describe.

        """

        self._validate_pkg(pkg_dict)
        self.pkg_dict = pkg_dict

    @classmethod
    def from_json(cls, filename: str):
        """
        Instantiate a Package object from a file.

        :param filename: Name of the JSON file
            that contains the description of the
            target package's API.

        """
        _log_info("Creating package from {}".format(filename))

        # read in output of "analyze.*" script
        with open(filename, 'r') as f:
            pkg_dict = json.loads(f.read())

        # validate
        return cls(pkg_dict)

    def _validate_pkg(self, pkg_dict: dict):

        assert isinstance(pkg_dict, dict)
        assert pkg_dict['name'] is not None
        assert pkg_dict['language'] is not None
        assert pkg_dict['functions'] is not None
        assert pkg_dict['classes'] is not None

        return

    def name(self):
        return(self.pkg_dict['name'])

    def num_functions(self):
        return(len(self.function_names()))

    def function_names(self):
        return(sorted(list(self.pkg_dict['functions'].keys())))

    def functions_with_args(self):
        return(self.pkg_dict['functions'])

    def num_classes(self):
        return(len(self.class_names()))

    def class_names(self):
        return(sorted(list(self.pkg_dict['classes'].keys())))

    def public_methods(self, class_name):
        return(sorted(list(self.pkg_dict['classes'][class_name]['public_methods'].keys())))

    def public_method_args(self, class_name, method_name):
        return(list(self.pkg_dict['classes'][class_name]['public_methods'][method_name]['args']))
