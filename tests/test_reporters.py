import unittest
import os
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
        reporter._check_function_arg_names()
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
        reporter._check_function_arg_names()
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
        reporter._check_function_arg_names()
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
