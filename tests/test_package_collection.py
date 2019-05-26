import unittest
import os
from doppel import PackageCollection
from doppel import PackageAPI

TESTDATA_DIR = os.path.join('tests', 'testdata')


class TestPackageAPI(unittest.TestCase):

    py_pkg_file = os.path.join(
        TESTDATA_DIR,
        'python_package1.json'
    )
    r_pkg_file = os.path.join(
        TESTDATA_DIR,
        'r_package1.json'
    )

    def setUp(self):
        self.pkg_collection = PackageCollection(
            packages=[
                PackageAPI.from_json(self.py_pkg_file),
                PackageAPI.from_json(self.r_pkg_file)
            ]
        )

    def test_all_classes(self):
        """
        PackageCollection.all_classes() should work as expected
        for packages with identical classes
        """
        self.assertEqual(
            self.pkg_collection.all_classes(),
            ["LupeFiasco"]
        )

    def test_shared_classes(self):
        """
        PackageCollection.shared_classes() should work as expected
        for packages with identical classes
        """
        self.assertEqual(
            self.pkg_collection.shared_classes(),
            ["LupeFiasco"]
        )

    def test_non_shared_classes(self):
        """
        PackageCollection.non_shared_classes() should work as expected
        for packages with identical classes.
        """
        self.assertEqual(
            self.pkg_collection.non_shared_classes(),
            []
        )

    def test_all_functions(self):
        """
        PackageCollection.all_functions() should work as expected
        for packages with some overlapping functions
        """
        self.assertEqual(
            self.pkg_collection.all_functions(),
            ["playback"]
        )

    def test_shared_functions(self):
        """
        PackageCollection.shared_functions() should work as expected
        for packages with some overlapping functions
        """
        self.assertEqual(
            self.pkg_collection.shared_functions(),
            ["playback"]
        )

    def test_non_shared_functions(self):
        """
        PackageCollection.non_shared_functions() should work as expected
        for packages with some overlapping functions
        """
        self.assertEqual(
            self.pkg_collection.non_shared_functions(),
            []
        )

    def test_shared_methods_by_class(self):
        """
        PackageCollection.shared_methods_by_class() should work
        as expected for packages with slightly different
        class methods
        """
        shared = self.pkg_collection.shared_methods_by_class()
        self.assertEqual(list(shared.keys()), ["LupeFiasco"])
        self.assertEqual(
            sorted(shared["LupeFiasco"]),
            sorted(["~~CONSTRUCTOR~~", "coast"])
        )

    def test_same_names(self):
        """
        PackageCollection should reject attempts
        to add two packages with the same name
        """
        self.assertRaisesRegex(
            ValueError,
            "All packages provided to PackageCollection must have unique names",
            lambda: PackageCollection(
                packages=[
                    PackageAPI.from_json(self.py_pkg_file),
                    PackageAPI.from_json(self.py_pkg_file)
                ]
            )
        )
