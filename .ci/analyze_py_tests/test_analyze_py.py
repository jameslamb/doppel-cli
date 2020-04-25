
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
    output_dir = "../../test_data"

    def _test_analyze(self, arg_list, pkg_name):
        args = doppel_analyze.parse_args(arg_list)
        res = doppel_analyze.do_everything(args)

        out_file = os.path.join(self.output_dir, "python_" + pkg_name + ".json")
        with open(out_file, 'r') as f:
            result = json.loads(f.read())
            assert isinstance(result, dict)

    def test_everything(self):
        """analyze.py should work"""
        for pkg_name in self.TEST_PACKAGES:
            self._test_analyze(
                [
                    "--pkg", pkg_name,
                    "--output_dir", self.output_dir,
                    "--kwargs-string", "~~kwargs~~",
                    "--constructor-string", "~~CONSTRUCTOR~~"
                ],
                pkg_name
            )

    def test_verbose(self):
        """
        doppel-describe --verbose should work
        """
        for pkg_name in self.TEST_PACKAGES:
            self._test_analyze(
                [
                    "--pkg", pkg_name,
                    "--output_dir", self.output_dir,
                    "--kwargs-string", "~~kwargs~~",
                    "--constructor-string", "~~CONSTRUCTOR~~",
                    "--verbose"
                ],
                pkg_name
            )
