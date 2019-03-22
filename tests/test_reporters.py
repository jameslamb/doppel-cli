import unittest
import copy
from doppel import SimpleReporter
from doppel import PackageAPI
from doppel import DoppelTestError

BASE_PACKAGE = {
    "name": "pkg1",
    "language": "python",
    "functions": {
        "playback": {
            "args": [
                "bpm",
                "bass"
            ]
        },
        "reverse": {
            "args": [
                "x",
                "y",
                "z"
            ]
        },
        "split_channels": {
            "args": [
                "keep_list",
                "exclude_list"
            ]
        }
    },
    "classes": {}
}

PACKAGE_WITH_DIFFERENT_ARG_NUMBER = copy.deepcopy(BASE_PACKAGE)
PACKAGE_WITH_DIFFERENT_ARG_NUMBER['name'] = 'pkg2'
PACKAGE_WITH_DIFFERENT_ARG_NUMBER['functions']['playback']['args'].append('other')

PACKAGE_WITH_DIFFERENT_ARGS = copy.deepcopy(BASE_PACKAGE)
PACKAGE_WITH_DIFFERENT_ARGS['name'] = 'pkg2'
PACKAGE_WITH_DIFFERENT_ARGS['functions']['playback']['args'] = ['bass', 'beats_per_minute']

PACKAGE_WITH_DIFFERENT_ARG_ORDER = copy.deepcopy(BASE_PACKAGE)
PACKAGE_WITH_DIFFERENT_ARG_ORDER['name'] = 'pkg2'
PACKAGE_WITH_DIFFERENT_ARG_ORDER['functions']['playback']['args'] = ['bass', 'bpm']

PACKAGE_SUPER_DIFFERENT = copy.deepcopy(BASE_PACKAGE)
PACKAGE_SUPER_DIFFERENT['name'] = 'pkg2'
PACKAGE_SUPER_DIFFERENT['functions']['playback']['args'] = ['stuff', 'things', 'bass']

PACKAGE_EMPTY = {
    "name": "empty_pkg",
    "language": "python",
    "functions": {},
    "classes": {}
}


PACKAGE_BEEFY = copy.deepcopy(BASE_PACKAGE)
for i in range(5):
    func_name = "function_" + str(i)
    PACKAGE_BEEFY['functions'][func_name] = {
        "args": ["x", "y", "z"]
    }

    class_name = "class_" + str(i)
    PACKAGE_BEEFY['classes'][class_name] = {
        'public_methods': {
            k: {
                "args": ["thing", "stuff", "ok"]
            }
            for k in ["get", "push", "delete"]
        }
    }


class TestSimpleReporter(unittest.TestCase):

    def test_function_arg_number(self):
        """
        SimpleReporter should catch the condition where
        function implementations in two packages have different
        number of keyword arguments
        """
        reporter = SimpleReporter(
            pkgs=[PackageAPI(BASE_PACKAGE), PackageAPI(PACKAGE_WITH_DIFFERENT_ARG_NUMBER)],
            errors_allowed=100
        )
        reporter._check_function_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 1,
        )
        self.assertTrue(
            all([isinstance(x, DoppelTestError) for x in errors])
        )
        self.assertTrue(
            errors[0].msg == "Function 'playback()' exists in all packages but with differing number of arguments (2,3)."
        )

    def test_function_args(self):
        """
        SimpleReporter should catch the condition where
        function implementations in two packages have different
        different arguments (even if they have the same number
        of arguments)
        """
        reporter = SimpleReporter(
            pkgs=[PackageAPI(BASE_PACKAGE), PackageAPI(PACKAGE_WITH_DIFFERENT_ARGS)],
            errors_allowed=100
        )
        reporter._check_function_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 1,
        )
        self.assertTrue(
            all([isinstance(x, DoppelTestError) for x in errors])
        )
        self.assertTrue(
            errors[0].msg == "Function 'playback()' exists in all packages but some arguments are not shared in all implementations."
        )

    def test_function_arg_order(self):
        """
        SimpleReporter should catch errors of the form
        'this function has the same keyword args in
        both packages but they are in different orders'
        """
        reporter = SimpleReporter(
            pkgs=[PackageAPI(BASE_PACKAGE), PackageAPI(PACKAGE_WITH_DIFFERENT_ARG_ORDER)],
            errors_allowed=100
        )
        reporter._check_function_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 1,
        )
        self.assertTrue(
            all([isinstance(x, DoppelTestError) for x in errors])
        )
        self.assertTrue(
            errors[0].msg == "Function 'playback()' exists in all packages but with differing order of keyword arguments."
        )

    def test_function_all_wrong(self):
        """
        SimpleReporter should only throw a single error
        if one package has a function with different args, more args
        and different order.
        """
        reporter = SimpleReporter(
            pkgs=[PackageAPI(BASE_PACKAGE), PackageAPI(PACKAGE_SUPER_DIFFERENT)],
            errors_allowed=100
        )
        reporter._check_function_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 1,
        )
        self.assertTrue(
            all([isinstance(x, DoppelTestError) for x in errors])
        )
        self.assertTrue(
            errors[0].msg.startswith("Function 'playback()' exists in all packages but with differing number of arguments")
        )

    def test_identical_functions(self):
        """
        SimpleReporter should not create any errors
        if the shared function is the same in both packages.
        """
        reporter = SimpleReporter(
            pkgs=[PackageAPI(BASE_PACKAGE), PackageAPI(BASE_PACKAGE)],
            errors_allowed=0
        )
        reporter._check_function_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 0,
        )

    def test_totally_empty(self):
        """
        SimpleReporter should be fine if two packages
        are totally empty.
        """
        reporter = SimpleReporter(
            pkgs=[PackageAPI(PACKAGE_EMPTY), PackageAPI(PACKAGE_EMPTY)],
            errors_allowed=0
        )
        reporter._check_function_args()
        self.assertTrue(reporter.errors == [])

    def test_smoke_test(self):
        """
        SimpleReporter should run end-to-end without error
        """
        reporter = SimpleReporter(
            pkgs=[PackageAPI(PACKAGE_BEEFY), PackageAPI(PACKAGE_SUPER_DIFFERENT)],
            errors_allowed=100
        )

        # SimpleReporter has a sys.exit() in it. Mock that out
        def f():
            pass
        reporter._respond = f

        # check packages
        reporter.compare()
        self.assertTrue(True)

    def test_other_smoke_test(self):
        """
        SimpleReporter should run end-to-end without error. This test
        compares a package to itself (to get basic coverage of code that works
        on shared classes and functions)
        """
        reporter = SimpleReporter(
            pkgs=[PackageAPI(PACKAGE_BEEFY), PackageAPI(PACKAGE_BEEFY)],
            errors_allowed=100
        )

        # SimpleReporter has a sys.exit() in it. Mock that out
        def f():
            pass
        reporter._respond = f

        # check packages
        reporter.compare()
        self.assertTrue(True)
