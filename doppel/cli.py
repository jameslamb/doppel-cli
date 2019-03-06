
import click
import json
from doppel.reporters import SimpleReporter
from doppel.PackageAPI import PackageAPI


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
def main(files, errors_allowed: int):
    """
    doppel is a a continuous integration tool for testing
    the continuity of APIs for libraries implemented in
    different languages.

    :param errors_allowed: Number of errors that are
        permissible before throwing a non-zero exit
        code. Set this to a higher value to make doppel-cli
        more permissive.

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
