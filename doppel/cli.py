
import click
import json
from doppel.reporters import SimpleReporter


def _log_info(msg):
    print(msg)


class PackageAPI():
    """
    This class is used to hold the interface of a given package
    being analyzed by doppel. It's comparison operators enable comparison
    between interfaces and its standard JSON format allows this comparison
    to happen across programming languages.
    """

    def __init__(self, pkg_dict):

        self._validate_pkg(pkg_dict)
        self.pkg_dict = pkg_dict
        pass

    @classmethod
    def from_json(cls, filename):
        """
        Instantiate a Package object from a file.
        """
        _log_info("Creating package from {}".format(filename))

        # read in output of "analyze.*" script
        with open(filename, 'r') as f:
            pkg_dict = json.loads(f.read())

        # validate
        return cls(pkg_dict)

    def _validate_pkg(self, pkg_dict):

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
        return(list(self.pkg_dict['functions'].keys()))

    def functions_with_args(self):
        return(self.pkg_dict['functions'])

    def num_classes(self):
        return(len(self.class_names()))

    def class_names(self):
        return(list(self.pkg_dict['classes'].keys()))


@click.command()
@click.option(
    '--files', '-f',
    help="Comma-delimited list of doppel output files."
)
@click.option(
    '--errors-allowed',
    default=0,
    help="Integer number of errors to allow before returning non-zero exit code. Default is 0."
)
def main(files, errors_allowed):
    """
    doppel is a a continuous integration tool for testing
    the continuity of APIs for libraries implemented in
    different languages.
    """
    print("Loading comparison files")

    f_list = files.split(',')

    # Check if these are legit package objects
    pkgs = [PackageAPI.from_json(f) for f in f_list]

    # Report
    reporter = SimpleReporter(pkgs, errors_allowed)
    reporter.compare()


if __name__ == "__main__":
    main()
