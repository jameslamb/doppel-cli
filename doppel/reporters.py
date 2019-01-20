import sys
import doppel
from sys import stdout
from tabulate import tabulate
from functools import reduce
from typing import List


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

    def __init__(self, rows: list, headers: list):
        self.rows = rows
        self.headers = headers

    def write(self):
        stdout.write(tabulate(self.rows, self.headers, tablefmt="grid"))
        stdout.write('\n')


class SimpleReporter:

    errors = []
    exists_string = 'yes'
    absent_string = 'no'

    def __init__(self, pkgs: list, errors_allowed: int):
        """Default object used to manage doppel reporting

        This object implements the interface used by doppel-cli
        to handle reporting the status of a doppel-test run.

        :param pkgs: List of the package objects to report
            differences between.
        :param errors_allowed: Number of errors that are
            permissible before throwing a non-zero exit
            code. Set this to a higher value to make doppel-cli
            more permissive.

        """
        for pkg in pkgs:
            assert isinstance(pkg, doppel.PackageAPI)

        self.pkgs = pkgs
        self._errors_allowed = errors_allowed

    def compare(self):
        """
        Compare all the packages. This method will:
        * populate comparison data
        * print that data
        * return the appropriate exit code
        """

        # Checks (these print output as they're run)
        self._check_function_count()
        self._check_function_names()
        self._check_function_arg_names()

        self._check_class_count()
        self._check_class_names()

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

        # Only throw a non-zero exit code if you had too many errors
        sys.exit(max(0, num_errors - self._errors_allowed))

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
            pkg_names.append(pkg.name())
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
        """
        Check consistency between names of functions. Looking
        for errors of the form "function F does not exist
        in all packages".
        """

        stdout.write("\nFunction Names\n")
        stdout.write("==============\n")

        pkg_names = []
        functions_by_package = {}
        for pkg in self.pkgs:
            pkg_name = pkg.name()
            pkg_names.append(pkg_name)
            functions_by_package[pkg_name] = pkg.function_names()

        # Headers are easy moeny
        headers = ['function_name'] + [pkg.name() for pkg in self.pkgs]

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
                    row += [self.exists_string]
                else:
                    row += [self.absent_string]
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

    def _check_function_arg_names(self):
        """
        For each function that is in both packages, check
        whether the arguments to the functions differ.

        This method does not consider argument order.
        """
        stdout.write("\nFunction Argument Names\n")
        stdout.write("=======================\n")

        func_blocks_by_package = {}
        pkg_names = []
        shared_functions = None
        all_functions = set([])
        for pkg in self.pkgs:
            funcs = pkg.functions_with_args()
            func_blocks_by_package[pkg.name()] = funcs
            pkg_names.append(pkg.name())
            func_names = funcs.keys()

            for func_name in func_names:
                all_functions.add(func_name)

            if shared_functions is None:
                shared_functions = set(func_names)
            else:
                shared_functions = shared_functions.intersection(set(func_names))

        # If there are no shared functions, skip
        if len(shared_functions) == 0:
            stdout.write('No shared functions.\n')
            return

        headers = ['function_name', 'identical api?']
        rows = []

        for func_name in shared_functions:
            args = [func_blocks_by_package[p][func_name]['args'] for p in pkg_names]

            # check 1: same number of arguments?
            same_length = reduce(lambda a, b: len(a) == len(b), args)
            if not same_length:
                error_txt = "Function '{}()' exists in all packages but with differing number of arguments ({})."
                error_txt = error_txt.format(
                    func_name,
                    ",".join([str(len(a)) for a in args])
                )
                self.errors.append(DoppelTestError(error_txt))
                rows.append([func_name, 'no'])
                continue

            # check 2: same set of arguments
            same_args = reduce(lambda a, b: sorted(a) == sorted(b), args)
            if not same_args:
                error_txt = "Function '{}()' exists in all packages but with differing set of keyword arguments."
                self.errors.append(DoppelTestError(error_txt))
                rows.append([func_name, 'no'])
                continue

            # check 3: same set or arguments and same order
            same_order = reduce(lambda a, b: a == b, args)
            if not same_order:
                error_txt = "Function '{}()' exists in all packages but with differing order of keyword arguments."
                self.errors.append(DoppelTestError(error_txt))
                rows.append([func_name, 'no'])
                continue

            # if you get here, we're gucci
            rows.append([func_name, 'yes'])

        # Report output
        stdout.write('\n{} or the {} functions shared across all packages have identical signatures\n\n'.format(
            len([r for r in filter(lambda x: x[1] == 'yes', rows)]),
            len(all_functions)
        ))

        out = OutputTable(headers=headers, rows=rows)
        out.write()

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
            names.append(pkg.name())
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
        """
        Check consistency between names of classes. Looking
        for errors of the form "class X does not exist
        in all packages".
        """

        stdout.write("\nClass Names\n")
        stdout.write("===========\n")

        pkg_names = []
        classes_by_package = {}
        for pkg in self.pkgs:
            pkg_name = pkg.name()
            pkg_names.append(pkg_name)
            classes_by_package[pkg_name] = pkg.class_names()

        # Headers are easy moeny
        headers = ['class_name'] + [pkg.name() for pkg in self.pkgs]

        # Build up the rows. This is slow but w/e it works.
        all_classes = set([])
        for _, v in classes_by_package.items():
            for name in v:
                all_classes.add(name)

        classes_not_shared_by_all_pkgs = set([])
        rows = []
        for class_name in all_classes:
            row = [class_name]
            for pkg_name in pkg_names:
                if class_name in classes_by_package[pkg_name]:
                    row += [self.exists_string]
                else:
                    row += [self.absent_string]
                    classes_not_shared_by_all_pkgs.add(class_name)
            rows += [row]

        # Report output
        out = OutputTable(headers=headers, rows=rows)
        out.write()

        # Append errors
        if len(classes_not_shared_by_all_pkgs) > 0:
            for class_name in classes_not_shared_by_all_pkgs:
                error_txt = "Class '{}' is not exported by all packages".format(class_name)
                self.errors.append(DoppelTestError(error_txt))

        # Print output
        stdout.write("\n")
