import unittest
import copy
import re
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

BASE_PACKAGE2 = copy.deepcopy(BASE_PACKAGE)
BASE_PACKAGE2['name'] = 'pkg2'

# testing different function stuff
PACKAGE_WITH_DIFFERENT_ARG_NUMBER = copy.deepcopy(BASE_PACKAGE)
PACKAGE_WITH_DIFFERENT_ARG_NUMBER['name'] = 'pkg2'
PACKAGE_WITH_DIFFERENT_ARG_NUMBER['functions']['playback']['args'].append('other')

PACKAGE_WITH_DIFFERENT_ARGS = copy.deepcopy(BASE_PACKAGE)
PACKAGE_WITH_DIFFERENT_ARGS['name'] = 'pkg2'
PACKAGE_WITH_DIFFERENT_ARGS['functions']['playback']['args'] = ['bass', 'beats_per_minute']

PACKAGE_WITH_DIFFERENT_ARG_ORDER = copy.deepcopy(BASE_PACKAGE)
PACKAGE_WITH_DIFFERENT_ARG_ORDER['name'] = 'pkg2'
PACKAGE_WITH_DIFFERENT_ARG_ORDER['functions']['playback']['args'] = ['bass', 'bpm']

# testing different public method stuff
BASE_PACKAGE_WITH_CLASSES = copy.deepcopy(BASE_PACKAGE)
BASE_PACKAGE_WITH_CLASSES['classes'] = {
    'WaleFolarin': {
        'public_methods': {
            '~~CONSTRUCTOR~~': {
                'args': [
                    'x',
                    'y',
                    'z'
                ]
            },
            'no_days_off': {
                'args': [
                    'days_to_take',
                    'songs_to_record'
                ]
            }
        }
    }
}

PACKAGE_WITH_DIFFERENT_PM_ARG_NUMBER = copy.deepcopy(BASE_PACKAGE_WITH_CLASSES)
PACKAGE_WITH_DIFFERENT_PM_ARG_NUMBER['name'] = 'pkg2'
PACKAGE_WITH_DIFFERENT_PM_ARG_NUMBER['classes']['WaleFolarin']['public_methods']['no_days_off']['args'].append('about_nothing')

PACKAGE_WITH_DIFFERENT_PM_ARGS = copy.deepcopy(BASE_PACKAGE_WITH_CLASSES)
PACKAGE_WITH_DIFFERENT_PM_ARGS['name'] = 'pkg3'
PACKAGE_WITH_DIFFERENT_PM_ARGS['classes']['WaleFolarin']['public_methods']['no_days_off']['args'] = ['days_to_take', 'outchyea']

PACKAGE_WITH_DIFFERENT_PM_ARG_ORDER = copy.deepcopy(BASE_PACKAGE_WITH_CLASSES)
PACKAGE_WITH_DIFFERENT_PM_ARG_ORDER['name'] = 'pkg4'
PACKAGE_WITH_DIFFERENT_PM_ARG_ORDER['classes']['WaleFolarin']['public_methods']['no_days_off']['args'] = ['songs_to_record', 'days_to_take']

# super different
PACKAGE_SUPER_DIFFERENT = copy.deepcopy(BASE_PACKAGE)
PACKAGE_SUPER_DIFFERENT['name'] = 'pkg2'
PACKAGE_SUPER_DIFFERENT['functions']['playback']['args'] = ['stuff', 'things', 'bass']

PACKAGE_EMPTY = {
    "name": "empty_pkg",
    "language": "python",
    "functions": {},
    "classes": {}
}
PACKAGE_EMPTY2 = copy.deepcopy(PACKAGE_EMPTY)
PACKAGE_EMPTY2['name'] = 'pkg2'


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

PACKAGE_BEEFY2 = copy.deepcopy(PACKAGE_BEEFY)
PACKAGE_BEEFY2['name'] = 'pkg2'

PACKAGE_DIFFERENT_METHODS_1 = {
    "name": "py_pkg",
    "language": "python",
    "functions": {},
    "classes": {
        "SomeClass": {
            "public_methods": {
                "~~CONSTRUCTOR~~": {
                    "args": []
                },
                "write_py": {
                    "args": ["x", "y"]
                }
            }
        }
    }
}
PACKAGE_DIFFERENT_METHODS_2 = copy.deepcopy(PACKAGE_DIFFERENT_METHODS_1)
del PACKAGE_DIFFERENT_METHODS_2['classes']['SomeClass']['public_methods']['write_py']
PACKAGE_DIFFERENT_METHODS_2['classes']['SomeClass']['public_methods'].update({
    "write_r": {
        "args": ["x", "y"]
    }
})
PACKAGE_DIFFERENT_METHODS_2.update({
    "name": "r_pkg"
})


class TestSimpleReporter(unittest.TestCase):

    def test_function_arg_number(self):
        """
        SimpleReporter should catch the condition where
        function implementations in two packages have different
        number of keyword arguments.
        """
        reporter = SimpleReporter(
            pkgs=[
                PackageAPI(BASE_PACKAGE),
                PackageAPI(PACKAGE_WITH_DIFFERENT_ARG_NUMBER)
            ],
            errors_allowed=100
        )
        reporter._check_function_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 3
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
            pkgs=[
                PackageAPI(BASE_PACKAGE),
                PackageAPI(PACKAGE_WITH_DIFFERENT_ARGS)
            ],
            errors_allowed=100
        )
        reporter._check_function_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 2
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
            pkgs=[
                PackageAPI(BASE_PACKAGE),
                PackageAPI(PACKAGE_WITH_DIFFERENT_ARG_ORDER)
            ],
            errors_allowed=100
        )
        reporter._check_function_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 1
        )
        self.assertTrue(
            all([isinstance(x, DoppelTestError) for x in errors])
        )
        self.assertTrue(
            errors[0].msg == "Function 'playback()' exists in all packages but with differing order of keyword arguments."
        )

    def test_function_all_wrong(self):
        """
        SimpleReporter should throw 3 errors
        if one package has a function with different args, more args
        and different order.
        """
        reporter = SimpleReporter(
            pkgs=[
                PackageAPI(BASE_PACKAGE),
                PackageAPI(PACKAGE_SUPER_DIFFERENT)
            ],
            errors_allowed=100
        )
        reporter._check_function_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 3
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
            pkgs=[
                PackageAPI(BASE_PACKAGE),
                PackageAPI(BASE_PACKAGE2)
            ],
            errors_allowed=0
        )
        reporter._check_function_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 0
        )

    def test_public_method_arg_number(self):
        """
        SimpleReporter should catch the condition where
        public method implementations (same method, same class)
        in two packages have different number of keyword arguments
        """
        reporter = SimpleReporter(
            pkgs=[
                PackageAPI(BASE_PACKAGE_WITH_CLASSES),
                PackageAPI(PACKAGE_WITH_DIFFERENT_PM_ARG_NUMBER)
            ],
            errors_allowed=100
        )
        reporter._check_class_public_method_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 3
        )
        self.assertTrue(
            all([isinstance(x, DoppelTestError) for x in errors])
        )
        self.assertTrue(
            errors[0].msg == "Public method 'no_days_off()' on class 'WaleFolarin' exists in all packages but with differing number of arguments (2,3)."
        )

    def test_public_method_args(self):
        """
        SimpleReporter should catch the condition where
        public method implementations (same method, same class)
        in two packages have different different arguments (even if
        they have the same number of arguments)
        """
        reporter = SimpleReporter(
            pkgs=[
                PackageAPI(BASE_PACKAGE_WITH_CLASSES),
                PackageAPI(PACKAGE_WITH_DIFFERENT_PM_ARGS)
            ],
            errors_allowed=100
        )
        reporter._check_class_public_method_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 2
        )
        self.assertTrue(
            all([isinstance(x, DoppelTestError) for x in errors])
        )
        self.assertTrue(
            errors[0].msg == "Public method 'no_days_off()' on class 'WaleFolarin' exists in all packages but some arguments are not shared in all implementations."
        )

    def test_public_method_arg_order(self):
        """
        SimpleReporter should catch errors of the form
        'this function has the same keyword args in
        both packages but they are in different orders'
        """
        reporter = SimpleReporter(
            pkgs=[
                PackageAPI(BASE_PACKAGE_WITH_CLASSES),
                PackageAPI(PACKAGE_WITH_DIFFERENT_PM_ARG_ORDER)
            ],
            errors_allowed=100
        )
        reporter._check_class_public_method_args()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 1
        )
        self.assertTrue(
            all([isinstance(x, DoppelTestError) for x in errors])
        )
        self.assertTrue(
            errors[0].msg == "Public method 'no_days_off()' on class 'WaleFolarin' exists in all packages but with differing order of keyword arguments."
        )

    def test_different_public_methods(self):
        """
        SimpleReporter should handle the case where a class exists
        in both packages, with the same number of public methods,
        but with different methods.
        """
        reporter = SimpleReporter(
            pkgs=[
                PackageAPI(PACKAGE_DIFFERENT_METHODS_1),
                PackageAPI(PACKAGE_DIFFERENT_METHODS_2)
            ],
            errors_allowed=2
        )
        reporter._check_class_public_methods()
        errors = reporter.errors
        self.assertTrue(
            len(errors) == 2
        )
        self.assertTrue(
            all([isinstance(x, DoppelTestError) for x in errors])
        )
        self.assertTrue(
            errors[0].msg.startswith("Not all implementations of class 'SomeClass' have public method")
        )

    def test_totally_empty(self):
        """
        SimpleReporter should be fine if two packages
        are totally empty.
        """
        reporter = SimpleReporter(
            pkgs=[
                PackageAPI(PACKAGE_EMPTY),
                PackageAPI(PACKAGE_EMPTY2)
            ],
            errors_allowed=0
        )
        reporter._check_function_args()
        self.assertTrue(reporter.errors == [])

    def test_smoke_test(self):
        """
        SimpleReporter should run end-to-end without error
        """
        reporter = SimpleReporter(
            pkgs=[
                PackageAPI(PACKAGE_BEEFY),
                PackageAPI(PACKAGE_SUPER_DIFFERENT)
            ],
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
            pkgs=[
                PackageAPI(PACKAGE_BEEFY),
                PackageAPI(PACKAGE_BEEFY2)
            ],
            errors_allowed=100
        )

        # SimpleReporter has a sys.exit() in it. Mock that out
        def f():
            pass
        reporter._respond = f

        # check packages
        reporter.compare()
        self.assertTrue(True)

    def test_works_with_one_package(self):
        """
        SimpleReporter should not return any errors if you
        only use a single package
        """
        reporter = SimpleReporter(
            pkgs=[
                PackageAPI(BASE_PACKAGE_WITH_CLASSES)
            ],
            errors_allowed=0
        )

        # SimpleReporter has a sys.exit() in it. Mock that out
        def f():
            pass
        reporter._respond = f

        # check packages
        reporter.compare()
        self.assertTrue(len(reporter.pkgs) == 1)
        self.assertTrue(reporter.errors == [])

    def test_works_with_three_packages(self):
        """
        SimpleReporter should work correctly if you have
        three packages
        """
        reporter = SimpleReporter(
            pkgs=[
                PackageAPI(BASE_PACKAGE_WITH_CLASSES),
                PackageAPI(PACKAGE_WITH_DIFFERENT_PM_ARG_ORDER),
                PackageAPI(PACKAGE_WITH_DIFFERENT_PM_ARG_NUMBER)
            ],
            errors_allowed=100
        )

        # SimpleReporter has a sys.exit() in it. Mock that out
        def f():
            pass
        reporter._respond = f

        # check packages
        reporter.compare()

        # This check (exactly 3 errors) is important. To be sure
        # that other problems aren't getting silenced by short-circuiting
        self.assertTrue(len(reporter.errors) == 3)
        self.assertTrue(len(reporter.pkgs) == 3)

        # at least one should be the number-of-arguments error
        self.assertTrue(
            any([
                bool(re.search('differing number of arguments', err.msg))
                for err in reporter.errors
            ])
        )

        # at least one should be the some-args-not-shared
        self.assertTrue(
            any([
                bool(re.search('some arguments are not shared', err.msg))
                for err in reporter.errors
            ])
        )

        # at least one should be the different-order one
        self.assertTrue(
            any([
                bool(re.search('differing order of keyword arguments', err.msg))
                for err in reporter.errors
            ])
        )

    def test_works_with_ten_packages(self):
        """
        SimpleReporter should work correctly if you have
        ten packages (yes I know this is extreme)
        """
        pkgs = [
            PackageAPI(BASE_PACKAGE_WITH_CLASSES),
            PackageAPI(PACKAGE_WITH_DIFFERENT_PM_ARG_ORDER),
            PackageAPI(PACKAGE_WITH_DIFFERENT_PM_ARG_NUMBER)
        ]
        for i in range(7):
            new_pkg = copy.deepcopy(BASE_PACKAGE_WITH_CLASSES)
            new_pkg['name'] = 'test_package_' + str(i)
            pkgs.append(PackageAPI(new_pkg))

        reporter = SimpleReporter(
            pkgs=pkgs,
            errors_allowed=100
        )

        # SimpleReporter has a sys.exit() in it. Mock that out
        def f():
            pass
        reporter._respond = f

        # check packages
        reporter.compare()

        # This check (exactly 3 errors) is important. To be sure
        # that other problems aren't getting silenced by short-circuiting
        self.assertTrue(len(reporter.errors) == 3)
        self.assertTrue(len(reporter.pkgs) == 10)

        # at least one should be the number-of-arguments error
        self.assertTrue(
            any([
                bool(re.search('differing number of arguments', err.msg))
                for err in reporter.errors
            ])
        )

        # at least one should be the some-args-not-shared
        self.assertTrue(
            any([
                bool(re.search('some arguments are not shared', err.msg))
                for err in reporter.errors
            ])
        )

        # at least one should be the different-order one
        self.assertTrue(
            any([
                bool(re.search('differing order of keyword arguments', err.msg))
                for err in reporter.errors
            ])
        )
