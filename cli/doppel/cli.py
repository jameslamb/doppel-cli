
import click
import json


class PackageAPI():
    """
    This class is used to hold the interface of a given package
    being analyzed by doppel. It's comparison operators enable comparison
    between interfaces and its standard JSON format allows this comparison
    to happen across programming languages.
    """

    def __init__(self):
        pass

    @classmethod
    def from_json(self, filename):

        # read in output of "analyze.*" script
        with open(filename, 'r') as f:
            pkg_dict = json.loads(f.read())

        # validate
        return PackageAPI(pkg_dict)

    def _validate_pkg(self, pkg_dict):
        pass


@click.command()
@click.option(
    '--files', '-f',
    help="Comma-delimited list of doppel output files."
)
def main(files):
    """
    doppel is a a clntinuous integration tool for testing
    the continuity of APIs for libraries implemented in
    different languages.
    """
    print("Loading comparison files")

    f_list = files.split(',')
    for (f in f_list):
        print(f)

if __name__ == "__main__":
    main()
