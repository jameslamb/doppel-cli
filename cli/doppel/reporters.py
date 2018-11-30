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
        stdout.write('\n')


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
        self._check_function_names()

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

            stdout.write("\nTest Failures ({})\n".format(num_errors))
            stdout.write("===================\n")
            for err in self.errors:
                stdout.write("{}. {}\n".format(i, str(err)))
                i += 1

        sys.exit(num_errors)

    def _check_function_count(self):
        """
        Check consistency between exported functions
        """

        stdout.write("\nFunction Count\n")
        stdout.write("==============\n")

        # Compare number of functions
        pkg_names = []
        counts = []
        for pkg in self.pkgs:
            pkg_names.append(pkg.pkg_dict['name'])
            counts.append(pkg.num_functions())

        # Report output
        out = OutputTable(headers=pkg_names, rows=[counts])
        out.write()

        # Append errors
        if len(set(counts)) > 1:
            error_txt = "Packages have different counts of public functions! {}"
            error_txt = error_txt.format(
                ", ".join(["{} ({})".format(x, y) for x, y in zip(pkg_names, counts)])
            )
            self.errors.append(DoppelTestError(error_txt))

        # Print output
        stdout.write("\n")

    def _check_function_names(self):

        pkg_names = []
        functions_by_package = {}
        for pkg in self.pkgs:
            pkg_name = pkg.pkg_dict['name']
            pkg_names.append(pkg_name)
            functions_by_package[pkg_name] = pkg.function_names()

        # Headers are easy moeny
        headers = ['function_name'] + [pkg.pkg_dict['name'] for pkg in self.pkgs]

        # Build up the rows. This is slow but w/e it works.
        all_functions = set([])
        for _, v in functions_by_package.items():
            for name in v:
                all_functions.add(name)

        functions_not_shared_by_all_pkgs = set([])
        rows = []
        for func_name in all_functions:
            row = [func_name]
            for pkg_name in pkg_names:
                if func_name in functions_by_package[pkg_name]:
                    row += ['x']
                else:
                    row += ['---']
                    functions_not_shared_by_all_pkgs.add(func_name)
            rows += [row]

        # Report output
        out = OutputTable(headers=headers, rows=rows)
        out.write()

        # Append errors
        if len(functions_not_shared_by_all_pkgs) > 0:
            for func_name in functions_not_shared_by_all_pkgs:
                error_txt = "Function '{}()' is not exported by all packages".format(func_name)
                self.errors.append(DoppelTestError(error_txt))

        # Print output
        stdout.write("\n")

    def _check_class_count(self):
        """
        Check consistency between exported classes
        """

        stdout.write("\nClass Count\n")
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
                ", ".join(["{} ({})".format(x, y) for x, y in zip(names, counts)])
            )
            self.errors.append(DoppelTestError(error_txt))

        # Print output
        stdout.write("\n")

    def _check_class_names(self):
        raise NotImplementedError
