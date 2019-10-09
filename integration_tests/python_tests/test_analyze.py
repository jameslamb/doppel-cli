"""
integration tests on doppel-describe
commandline entrypoint (targeting a
python package)
"""

import json
import os
import pytest

# details that will always be true of doppel-describe output
EXPECTED_TOP_LEVEL_KEYS = set([
    "name",
    "language",
    "functions",
    "classes"
])
NUM_TOP_LEVEL_KEYS = len(EXPECTED_TOP_LEVEL_KEYS)


@pytest.fixture()
def rundescribe():
    """
    run doppel-describe to generate output file
    """
    # there isn't a clean way to pass in
    # command-line args to test scripts, so
    # using environment variables
    test_packages = [
        'testpkguno',
        'testpkgdos',
        'testpkgtres',
        'pythonspecific'
    ]

    # Added this abomination because something about
    # os.getenv('TEST_PACKAGE_DIR') was resulting in a None
    test_data_dir = os.path.abspath('../../test_data')

    results = {}

    for package_name in test_packages:
        cmd = "doppel-describe --language python -p {} --data-dir {}".format(
            package_name,
            test_data_dir
        )

        exit_code = os.system(cmd)
        if exit_code != 0:
            msg = "doppel-describe exited with non-zero exit code: {}"
            raise RuntimeError(msg.format(exit_code))

        output_file = "python_{}.json".format(package_name)
        path_to_output_file = os.path.join(
            test_data_dir,
            output_file
        )
        with open(path_to_output_file, 'r') as f:
            result_json = json.loads(f.read())

        results[package_name] = result_json

    return results


class TestBasicContract:
    """
    Tests that check that basic truths about the
    JSON file produced by doppel-describe remain
    true.
    """

    def test_contract(self, rundescribe):
        """
        The JSON file produced by doppel-describe should have
        only the expected top-level dictionary keys
        """
        result_json = rundescribe['testpkguno']

        for top_level_key in EXPECTED_TOP_LEVEL_KEYS:
            assert result_json.get(top_level_key, False)
        assert len(result_json.keys()) == NUM_TOP_LEVEL_KEYS

    def test_name(self, rundescribe):
        """
        'name' should be a string
        """
        assert isinstance(rundescribe['testpkguno']['name'], str)

    def test_language(self, rundescribe):
        """
        'language' should be 'python'
        """
        assert rundescribe['testpkguno']['language'] == 'python'

    def test_functions_block(self, rundescribe):
        """
        'functions' should be a dictionary keyed
        by function name. Each function should have a dictionary keyed
        by 'args' where 'args' holds an array of strings.

        Nothing other than 'args' should be included in the
        function interface.
        """
        for func_name, func_interface in rundescribe['testpkguno']['functions'].items():
            args = func_interface['args']
            assert isinstance(args, list)
            assert len(func_interface.keys()) == 1
            if len(args) > 0:
                assert all([isinstance(x, str) for x in args])

    def test_classes_block(self, rundescribe):
        """
        'classes' should be a dictionary keyed
        by class name. Each of those classes should
        have a single section called 'public_methods'.
        Each method should have a dictionary keyed
        by 'args' where 'args' holds an array of strings.

        Nothing other than 'args' should be included in the
        method interface and nothing other than 'public_methods'
        should be included in the class interface.
        """
        for class_name, class_interface in rundescribe['testpkguno']['classes'].items():

            assert len(class_interface.keys()) == 1

            for method_name, method_interface in class_interface['public_methods'].items():
                args = method_interface['args']
                assert isinstance(args, list)
                assert len(method_interface.keys()) == 1
                if len(args) > 0:
                    assert all([isinstance(x, str) for x in args])


class TestFunctionStuff:
    """
    Tests that the "function" block of the JSON
    produced by doppel-describe is correct.
    """

    def test_functions_found(self, rundescribe):
        """
        Exported functions should all be found,
        even if decorators are used on them.

        No other stuff should end up in "functions".
        """
        func_dict = rundescribe['testpkguno']['functions']

        expected_functions = [
            'function_a',
            'function_b',
            'function_c'
        ]

        for f in expected_functions:
            assert func_dict.get(f, False)

        assert len(func_dict.keys()) == len(expected_functions)

    def test_empty_function(self, rundescribe):
        """
        Functions without any arguments should get an
        'args' dictionary with an empty list.
        """
        assert rundescribe['testpkguno']['functions']['function_a']['args'] == []

    def test_regular_function(self, rundescribe):
        """
        Functions with a mix of actual keyword args
        and '**kwargs' should have the correct signature.
        """
        expected = {
            "args": ['x', 'y', '~~KWARGS~~']
        }
        assert rundescribe['testpkguno']['functions']['function_b'] == expected

    def test_kwargs_only_function(self, rundescribe):
        """
        Functions with only '**kwargs' should have
        the correct signature.
        """
        expected = {
            "args": ['~~KWARGS~~']
        }
        assert rundescribe['testpkguno']['functions']['function_c'] == expected


class TestClassStuff:
    """
    Tests that the "classes" block of the JSON
    produced by doppel-describe is correct.
    """

    def test_classes_found(self, rundescribe):
        """
        Exported classes should all be found.
        """
        class_dict = rundescribe['testpkguno']['classes']

        expected_classes = [
            'ClassA',
            'ClassB',
            'ClassC',
            'ClassD',
            'ClassE',
            'ClassF'
        ]

        for c in expected_classes:
            assert class_dict.get(c, False)

        assert len(class_dict.keys()) == len(expected_classes)

    def test_class_public_methods_found(self, rundescribe):
        """
        Public class methods of all exported classes
        should be found.

        No other stuff should end up underneath classes
        within "classes".
        """
        class_dict = rundescribe['testpkguno']['classes']
        expected_methods = [
            '~~CONSTRUCTOR~~',
            'anarchy',
            'banarchy',
            'canarchy'
        ]

        for e in expected_methods:
            assert class_dict['ClassA']['public_methods'].get(e, False)

        assert len(class_dict['ClassA']['public_methods'].keys()) == len(expected_methods)

    def test_inherited_class_public_methods_found(self, rundescribe):
        """
        Public methods documented in the API of exported
        classes should include methods which are defined
        by a parent object and not overwritten by the
        child.

        No other stuff should end up underneath classes
        within "classes".
        """
        class_dict = rundescribe['testpkguno']['classes']
        expected_methods = [
            '~~CONSTRUCTOR~~',
            'anarchy',
            'banarchy',
            'canarchy',
            'hello_there'
        ]

        for e in expected_methods:
            assert class_dict['ClassB']['public_methods'].get(e, False)

        assert len(class_dict['ClassB']['public_methods'].keys()) == len(expected_methods)

    def test_classmethods_found(self, rundescribe):
        """
        Class methods should be correctly found and
        documented alongside other public methods in
        a class
        """
        assert rundescribe['testpkguno']['classes']['ClassC']['public_methods'].get('from_string', False)

    def test_inherited_classmethods_found(self, rundescribe):
        """
        Class methods inherited from a parent class
        should be correctly found and documented
        alongside other public methods in a class
        """
        assert rundescribe['testpkguno']['classes']['ClassD']['public_methods'].get('from_string', False)

    def test_empty_constructors(self, rundescribe):
        """
        Classes with constructors that have no keyword args
        should be serialized correctly
        """
        class_dict = rundescribe['testpkguno']['classes']
        expected_methods = [
            '~~CONSTRUCTOR~~',
            'from_string'
        ]

        for e in expected_methods:
            assert class_dict['ClassE']['public_methods'].get(e, False)

        # test that things with no kwargs produce "args": [], not "args": {}
        # expect_true(isTRUE(
        #    grepl('.+"ClassE".+~~CONSTRUCTOR~~.+"args"\\:\\[\\]', RESULTS[["testpkguno"]][["raw"]])
        # ))
        # expect_true(isTRUE(
        #     grepl('.+"from_string".+~~CONSTRUCTOR~~.+"args"\\:\\[\\]', RESULTS[["testpkguno"]][["raw"]])
        # ))

    def test_empty_classes(self, rundescribe):
        """
        Totally empty classes should still have their
        constructors documented
        """
        assert list(rundescribe['testpkguno']['classes']['ClassF']['public_methods'].keys()) == ['~~CONSTRUCTOR~~']
        assert rundescribe['testpkguno']['classes']['ClassF']['public_methods']['~~CONSTRUCTOR~~'] == {'args': []}


class TestFunctionOnly:
    """
    Test the behavior of analyze.py for packages
    which have functions but not classes
    """

    def test_top_level_keys(self, rundescribe):
        """
        The JSON file produce by doppel-describe
        should have only the expected top-level dictionary keys
        """
        result_json = rundescribe['testpkgdos']

        for top_level_key in EXPECTED_TOP_LEVEL_KEYS:
            assert result_json.get(top_level_key, None) is not None
        assert len(result_json.keys()) == NUM_TOP_LEVEL_KEYS


class TestClassOnly:
    """
    Test the behavior of analyze.py for packages
    which have classes but not functions
    """

    def test_top_level_keys(self, rundescribe):
        """
        The JSON file produce by doppel-describe
        should have only the expected top-level dictionary keys
        """
        result_json = rundescribe['testpkgtres']

        for top_level_key in EXPECTED_TOP_LEVEL_KEYS:
            assert result_json.get(top_level_key, None) is not None
        assert len(result_json.keys()) == NUM_TOP_LEVEL_KEYS


class PythonSpecific:
    """
    Test the behavior of analyze.py for packages
    with some Python-specific features like
    submodules and custom exceptions
    """

    def test_top_level_keys(self, rundescribe):
        """
        The JSON file produce by doppel-describe
        should have only the expected top-level dictionary keys
        """
        result_json = rundescribe['pythonspecific']

        for top_level_key in EXPECTED_TOP_LEVEL_KEYS:
            assert result_json.get(top_level_key, None) is not None
        assert len(result_json.keys()) == NUM_TOP_LEVEL_KEYS

    def test_sub_modules(self, rundescribe):
        """
        analyze.py should correctly handle python submodules and
        should ignore package constant.
        """
        result_json = rundescribe['pythonspecific']

        assert set(result_json['functions'].keys()) == set(['some_function'])
        assert set(result_json['classes'].keys()) == set(['SomeClass', 'GreatClass'])

    def test_inner_classes(self, rundescribe):
        """
        analyze.py should correctly handle classes
        that are included as members of another
        class
        """
        result_json = rundescribe['pythonspecific']

        assert set(result_json['classes']['GreatClass']['public_methods'].keys()) == set(['do_stuff', 'LilGreatClass'])
        lil_args = result_json['classes']['GreatClass']['public_methods']['LilGreatClass']
        assert set(lil_args) == ['things', 'stuff']
