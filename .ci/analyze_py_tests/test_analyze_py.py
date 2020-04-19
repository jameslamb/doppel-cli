
import json
import os

try:
    import doppel_analyze
except ModuleNotFoundError:
    from . import doppel_analyze


class TestAnalyzePy:

    TEST_PACKAGES = [
        "testpkguno",
        "testpkgdos",
        "testpkgtres",
        "pythonspecific"
    ]

    @staticmethod
    def _test_analyze(arg_list):
        args = doppel_analyze.parse_args(arg_list)
        res = doppel_analyze.do_everything(args)

        out_file = os.path.join(output_dir, "python_" + pkg_name + ".json")
        with open(out_file, 'r') as f:
            result = json.loads(f.read())
            assert isinstance(result, dict)

    def test_everything(self):
        """analyze.py should work"""
        output_dir = "../../test_data"
        for pkg_name in self.TEST_PACKAGES:
            self._test_analyze([
                "--pkg", pkg_name,
                "--output_dir", output_dir,
                "--kwargs-string", "~~kwargs~~",
                "--constructor-string", "~~CONSTRUCTOR~~"
            ])

    def test_verbose(self):
        """
        doppel-dsecribe --verbose should work
        """
        output_dir = "../../test_data"
        for pkg_name in self.TEST_PACKAGES:
            self._test_analyze([
                "--pkg", pkg_name,
                "--output_dir", output_dir,
                "--kwargs-string", "~~kwargs~~",
                "--constructor-string", "~~CONSTRUCTOR~~",
                "--verbose"
            ])
