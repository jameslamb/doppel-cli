import unittest
import os
from doppel import PackageAPI

TESTDATA_DIR = os.path.join('tests', 'testdata')


class TestPackageAPI(unittest.TestCase):
    """
    PackageAPI tests on simple package with
    one class and one or two functions
    """

    py_pkg_file = os.path.join(
        TESTDATA_DIR,
        'python_package1.json'
    )
    r_pkg_file = os.path.join(
        TESTDATA_DIR,
        'r_package1.json'
    )

    def test_from_json_py(self):
        """
        PackageAPI.from_json() should work for Python packages
        """
        pkg = PackageAPI.from_json(self.py_pkg_file)

        self.assertEqual(pkg.name(), 'boombap [python]')
        self.assertEqual(pkg.num_functions(), 1)
        self.assertEqual(pkg.function_names(), ['playback'])
        self.assertEqual(
            pkg.functions_with_args(),
            {
                'playback': {
                    'args': [
                        'bpm',
                        'bass'
                    ]
                }
            }
        )
        self.assertEqual(pkg.num_classes(), 1)
        self.assertEqual(pkg.class_names(), ["LupeFiasco"])
        self.assertEqual(pkg.public_methods("LupeFiasco"), ["coast", "~~CONSTRUCTOR~~"])
        self.assertEqual(
            pkg.public_method_args("LupeFiasco", "~~CONSTRUCTOR~~"),
            ["kick", "push"]
        )
        self.assertEqual(
            pkg.public_method_args("LupeFiasco", "coast"),
            []
        )

    def test_from_json_r(self):
        """
        PackageAPI.from_json() should work for R packages
        """
        pkg = PackageAPI.from_json(self.r_pkg_file)

        self.assertEqual(pkg.name(), 'boombap [r]')
        self.assertEqual(pkg.num_functions(), 1)
        self.assertEqual(pkg.function_names(), ['playback'])
        self.assertEqual(
            pkg.functions_with_args(),
            {
                'playback': {
                    'args': [
                        'bpm',
                        'bass'
                    ]
                }
            }
        )
        self.assertEqual(pkg.num_classes(), 1)
        self.assertEqual(pkg.class_names(), ["LupeFiasco"])
        self.assertEqual(pkg.public_methods("LupeFiasco"), ["coast", "words", "~~CONSTRUCTOR~~"])
        self.assertEqual(
            pkg.public_method_args("LupeFiasco", "~~CONSTRUCTOR~~"),
            ["kick", "push"]
        )
        self.assertEqual(
            pkg.public_method_args("LupeFiasco", "coast"),
            []
        )
        self.assertEqual(
            pkg.public_method_args("LupeFiasco", "words"),
            ["i_said", "i_never_said"]
        )
