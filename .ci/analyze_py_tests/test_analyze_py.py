
import json
import os

try:
    import doppel_analyze
except ModuleNotFoundError:
    from . import doppel_analyze


class TestAnalyzePy:

    def test_everything(self):
        """analyze.py should work"""
        TEST_PACKAGES = [
            "testpkguno",
            "testpkgdos",
            "testpkgtres"
        ]
        output_dir = "/Users/jlamb/repos/doppel-cli/test_data"
        for pkg_name in TEST_PACKAGES:
            args = doppel_analyze.parse_args([
                "--pkg", pkg_name,
                "--output_dir", output_dir,
                "--kwargs-string", "~~kwargs~~",
                "--constructor-string", "~~CONSTRUCTOR~~"
            ])
            res = doppel_analyze.do_everything(args)

            out_file = os.path.join(output_dir, "python_" + pkg_name + ".json")
            with open(out_file, 'r') as f:
                result = json.loads(f.read())
                assert isinstance(result, dict)
