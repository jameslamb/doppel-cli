import sys
import doppel
from sys import stdout
from tabulate import tabulate


class DoppelTestError:

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return("{}\n".format(self.msg))


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
        self._check_class_count()

        # Finally
        self._respond()

    def _respond(self):
        """
        After all evaluations, determine final exit status.

        This down here in a separate method so that it can later
        be extended to handle configuration like "skip these particular
        methods".
        """
        num_errors = len(self.errors)
        i = 1
        if num_errors > 0:

            stdout.write("\n\nTest Failures ({})\n".format(num_errors))
            stdout.write("===================\n")
            for err in self.errors:
                stdout.write("{}. {}\n".format(i, str(err)))
                i += 1

        sys.exit(num_errors)

    def _check_function_count(self):
        """
        Check consistency between exported functions
        """

        stdout.write("\n\nFunction Count\n")
        stdout.write("==============\n")

        # Compare number of functions
        names = []
        counts = []
        for pkg in self.pkgs:
            names.append(pkg.pkg_dict['name'])
            counts.append(pkg.num_functions())

        # Report output
        out = OutputTable(headers=names, rows=[counts])
        out.write()

        # Append errors
        if len(set(counts)) > 1:
            error_txt = "Packages have different counts of public functions! {}"
            error_txt = error_txt.format(
                ", ".join(["{} ({}])".format(x, y) for x, y in zip(names, counts)])
            )
            self.errors.append(DoppelTestError(error_txt))

        # Print output
        stdout.write("\n")

    def _check_function_names(self):
        raise NotImplementedError

    def _check_class_count(self):
        """
        Check consistency between exported classes
        """

        stdout.write("\n\nClass Count\n")
        stdout.write("===========\n")

        # Compare number of class
        names = []
        counts = []
        for pkg in self.pkgs:
            names.append(pkg.pkg_dict['name'])
            counts.append(pkg.num_classes())

        # Report output
        out = OutputTable(headers=names, rows=[counts])
        out.write()

        # Append errors
        if len(set(counts)) > 1:
            error_txt = "Packages have different counts of exported classes! {}"
            error_txt = error_txt.format(
                ["{} [{}]".format(x, y) for x, y in zip(names, counts)]
            )
            self.errors.append(DoppelTestError(error_txt))

        # Print output
        stdout.write("\n")

    def _check_method_names(self):
        raise NotImplementedError
