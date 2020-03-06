import sys
import doppel
from sys import stdout
from tabulate import tabulate
from functools import reduce
from doppel.DoppelTestError import DoppelTestError


class _OutputTable:
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
        """
        Write out a table of results to stdout.
        """
        stdout.write(tabulate(self.rows, self.headers, tablefmt="grid"))
        stdout.write('\n')


class SimpleReporter:

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

        self.errors = []
        self.exists_string = 'yes'
        self.absent_string = 'no'

        self.pkgs = pkgs
        self.pkg_collection = doppel.PackageCollection(pkgs)
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
        self._check_function_args()

        self._check_class_count()
        self._check_class_names()

        self._check_class_public_methods()
        self._check_class_public_method_args()

        # Finally
        self._respond()

    def _respond(self):  # pragma: no cover
        """
        After all evaluations, determine final exit status.

        This is down here in a separate method so that it can later
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
        out = _OutputTable(headers=pkg_names, rows=[counts])
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

        # Headers are easy money
        headers = ['function_name'] + [pkg.name() for pkg in self.pkgs]

        # Build up the rows. This is slow but w/e it works.
        all_functions = self.pkg_collection.all_functions()
        non_shared_functions = self.pkg_collection.non_shared_functions()

        rows = []
        for func_name in all_functions:
            row = [func_name]
            for pkg_name in pkg_names:
                if func_name in functions_by_package[pkg_name]:
                    row += [self.exists_string]
                else:
                    row += [self.absent_string]
            rows += [row]

        # Report output
        out = _OutputTable(headers=headers, rows=rows)
        out.write()

        # Append errors
        if len(non_shared_functions) > 0:
            for func_name in non_shared_functions:
                error_txt = "Function '{}()' is not exported by all packages".format(func_name)
                self.errors.append(DoppelTestError(error_txt))

        # Print output
        stdout.write("\n")

    def _check_function_args(self):
        """
        For each function that is in all packages, check
        whether the arguments to the functions differ.
        """
        stdout.write("\nFunction Argument Names\n")
        stdout.write("=======================\n")

        func_blocks_by_package = {
            pkg.name(): pkg.pkg_dict['functions']
            for pkg in self.pkgs
        }
        pkg_names = self.pkg_collection.package_names()
        shared_functions = self.pkg_collection.shared_functions()

        # If there are no shared functions, skip
        if len(shared_functions) == 0:
            stdout.write('No shared functions.\n')
            return

        headers = ['function_name', 'identical api?']
        rows = []

        for func_name in shared_functions:

            identical_api = 'yes'

            args = [
                func_blocks_by_package[p][func_name]['args']
                for p in pkg_names
            ]

            # check 1: same number of arguments?
            same_length = all([
                len(func_arg_list) == len(args[0])
                for func_arg_list in args
            ])
            if not same_length:
                error_txt = "Function '{}()' exists in all packages but with differing number of arguments ({})."
                error_txt = error_txt.format(
                    func_name,
                    ",".join([str(len(a)) for a in args])
                )
                self.errors.append(DoppelTestError(error_txt))
                identical_api = 'no'

            # check 2: same set of arguments
            same_args = all([
                sorted(func_arg_list) == sorted(args[0])
                for func_arg_list in args
            ])
            if not same_args:
                error_txt = "Function '{}()' exists in all packages but some arguments are not shared in all implementations."
                error_txt = error_txt.format(func_name)
                self.errors.append(DoppelTestError(error_txt))
                identical_api = 'no'

            # check 3: same set of arguments and same order
            same_order = all([
                len(func_arg_list) == len(args[0]) and func_arg_list == args[0]
                for func_arg_list in args
            ])
            if not same_order:
                error_txt = "Function '{}()' exists in all packages but with differing order of keyword arguments."
                error_txt = error_txt.format(func_name)
                self.errors.append(DoppelTestError(error_txt))
                identical_api = 'no'

            # if you get here, we're gucci
            rows.append([func_name, identical_api])

        # Report output
        stdout.write('\n{} of the {} functions shared across all packages have identical signatures\n\n'.format(
            len([r for r in filter(lambda x: x[1] == 'yes', rows)]),
            len(shared_functions)
        ))

        out = _OutputTable(headers=headers, rows=rows)
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
        out = _OutputTable(headers=names, rows=[counts])
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

        # Headers are easy money
        headers = ['class_name'] + [pkg.name() for pkg in self.pkgs]

        # Build up the rows. This is slow but w/e it works.
        all_classes = self.pkg_collection.all_classes()
        non_shared_classes = self.pkg_collection.non_shared_classes()

        rows = []
        for class_name in all_classes:
            row = [class_name]
            for pkg_name in pkg_names:
                if class_name in classes_by_package[pkg_name]:
                    row += [self.exists_string]
                else:
                    row += [self.absent_string]
            rows += [row]

        # Report output
        out = _OutputTable(headers=headers, rows=rows)
        out.write()

        # Append errors
        if len(non_shared_classes) > 0:
            for class_name in non_shared_classes:
                error_txt = "Class '{}' is not exported by all packages".format(class_name)
                self.errors.append(DoppelTestError(error_txt))

        # Print output
        stdout.write("\n")

    def _check_class_public_methods(self):
        """
        Check for consistency of public method names
        across different classes. Looking for errors
        of the form "class X has method y which does
        not exist on class X"
        """

        stdout.write("\nClass Public Methods\n")
        stdout.write("====================\n")

        shared_classes = self.pkg_collection.shared_classes()

        if len(shared_classes) == 0:
            stdout.write('No shared classes.\n')
            return

        # Figure out which methods are not shared across
        # all packages
        for class_name in shared_classes:
            shared_methods = set(
                self.pkgs[0].public_methods(class_name)
            )
            nonshared_methods = set([])

            for pkg in self.pkgs[1:]:
                methods = pkg.public_methods(class_name)
                diff = shared_methods.symmetric_difference(
                    methods
                )

                shared_methods = shared_methods.intersection(methods)
                for m in diff:
                    nonshared_methods.add(m)

            # If anything is in nonshared methods, add an error
            for method in nonshared_methods:
                error_txt = "Not all implementations of class '{}' have public method '{}()'".format(
                    class_name,
                    method
                )
                self.errors.append(DoppelTestError(error_txt))

    def _check_class_public_method_args(self):
        """
        Check for consistency of public method signatures
        (arguments) for shared public methods in shared
        classes
        """
        stdout.write("\nArguments in Class Public Methods\n")
        stdout.write("=================================\n")

        shared_classes = self.pkg_collection.shared_classes()
        if len(shared_classes) == 0:
            stdout.write('No shared classes.\n')
            return

        # Initialize the table
        headers = ['class.method', 'identical api?']
        rows = []

        shared_methods_by_class = self.pkg_collection.shared_methods_by_class()
        for class_name, methods in shared_methods_by_class.items():
            for method_name in methods:

                identical_api = 'yes'

                display_name = "{}.{}()".format(
                    class_name,
                    method_name
                )

                # Generate a list of lists of args
                args = [
                    pkg.public_method_args(class_name, method_name)
                    for pkg in self.pkgs
                ]

                # check 1: same number of arguments?
                same_length = all([
                    len(func_arg_list) == len(args[0])
                    for func_arg_list in args
                ])
                if not same_length:
                    error_txt = "Public method '{}()' on class '{}' exists in all packages but with differing number of arguments ({})."
                    error_txt = error_txt.format(
                        method_name,
                        class_name,
                        ",".join([str(len(a)) for a in args])
                    )
                    self.errors.append(DoppelTestError(error_txt))
                    identical_api = 'no'

                # check 2: same set of arguments
                same_args = all([
                    sorted(func_arg_list) == sorted(args[0])
                    for func_arg_list in args
                ])
                if not same_args:
                    error_txt = "Public method '{}()' on class '{}' exists in all packages but some arguments are not shared in all implementations."
                    error_txt = error_txt.format(
                        method_name,
                        class_name
                    )
                    self.errors.append(DoppelTestError(error_txt))
                    identical_api = 'no'

                # check 3: same set or arguments and same order
                same_order = all([
                    func_arg_list == args[0]
                    for func_arg_list in args
                ])
                if not same_order:
                    error_txt = "Public method '{}()' on class '{}' exists in all packages but with differing order of keyword arguments."
                    error_txt = error_txt.format(
                        method_name,
                        class_name
                    )
                    self.errors.append(DoppelTestError(error_txt))
                    identical_api = 'no'

                # if you get here, we're gucci
                rows.append([display_name, identical_api])

        # Report output
        out = _OutputTable(headers=headers, rows=rows)
        out.write()

        # Print output
        stdout.write("\n")
