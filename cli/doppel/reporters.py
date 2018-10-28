import sys
import doppel
from sys import stdout
from tabulate import tabulate


class DoppelTestError:

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        stdout.write("{}\n".format(self.msg))


class OutputTable:
    """
    Many checks will write tabular output. Wrapping
    this in a class so the choice of format from
    tabulate() is configurable without lots of code
    changes.

    Ref: https://pypi.org/project/tabulate/#description
    """
    def __init__(self, rows, headers):
        self.rows = rows
        self.headers = headers

    def write(self):
        stdout.write(tabulate(self.rows, self.headers, tablefmt="grid"))
        stdout.write('\n\n')


class SimpleReporter:

    errors = []

    def __init__(self, pkgs):

        for pkg in pkgs:
            assert isinstance(pkg, doppel.PackageAPI)

        self.pkgs = pkgs

    def compare(self):
        """
        Compare all the packages. This method will:
        * populate comparison data
        * print that data
        * return the appropriate exit code
        """

        # Checks (these print output as they're run)
        self._check_function_count()

        # Finally
        self._respond()

    def _respond(self):
        """
        After all evaluations, determine final exit status.

        This down here in a separate method so that it can later
        be extended to handle configuration like "skip these particular
        methods".
        """
        sys.exit(len(self.errors))

    def _check_function_count(self):
        """
        Check consistency between exported functions
        """

        stdout.write("\n\nFunction Count\n")
        stdout.write("==============\n")

        # Compare number of functions
        names = []
        function_counts = []
        for pkg in self.pkgs:
            names.append(pkg.pkg_dict['name'])
            function_counts.append(pkg.num_functions())

        # Report output
        out = OutputTable(headers=names, rows=[function_counts])
        out.write()

        # Append errors
        if len(set(function_counts)) > 1:
            error_txt = "Packages have different counts of public functions! {}"
            error_txt = error_txt.format(
                ["{} [{}]".format(x, y) for x, y in zip(names, function_counts)]
            )
            self.errors.append(DoppelTestError(error_txt))

        # Print output
        stdout.write("\n")

    def _check_function_names(self):
        raise NotImplementedError

    def _check_method_count(self):
        raise NotImplementedError

    def _check_method_names(self):
        raise NotImplementedError
