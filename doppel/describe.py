"""
Code for ``doppel-describe``. This code calls scripts in ``bin/``:

* ``analyze.py``: describe a Python package
* ``analyze.R``: describe an R package
"""

import logging
import os

from sys import stdout

import click
import pkg_resources

logger = logging.getLogger()
logging.basicConfig(format="%(levelname)s [%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


@click.command()
@click.option(
    "--language",
    "-l",
    default=None,
    help="Programming language. Currently python and R are supported.",
)
@click.option("--pkg_name", "-p", default=None, help="Name of a package")
@click.option(
    "--data-dir",
    "-d",
    default=None,
    help="Path to write output file to.",
)
@click.option(
    "--version", default=False, help="Get the current version of doppel-describe", is_flag=True
)
@click.option(
    "--verbose", is_flag=True, default=False, help="Use this flag to get more detailed logs"
)
def main(language: str, pkg_name: str, data_dir: str, version: bool, verbose: bool) -> None:
    """
    Generate a description of the public API for a software package and
    write out a JSON representation of it.
    """
    if version is True:
        version_file = os.path.join(os.path.dirname(__file__), "VERSION")
        with open(version_file, "r") as f:
            out = f.read()
        stdout.write(out)
        return

    if language is None:
        raise RuntimeError('Missing option "--language"')

    if pkg_name is None:
        raise RuntimeError('Missing option "--pkg_name"')

    if data_dir is None:
        raise RuntimeError('Missing option "--data-dir"')

    if verbose is True:
        logger.setLevel(logging.DEBUG)
        logger.debug("Running doppel-describe with verbose logging.")
    else:
        logger.setLevel(logging.INFO)

    language = language.lower()
    logger.info("Testing package {} [{}]".format(pkg_name, language))

    if not os.path.isdir(data_dir):
        msg = "Directory '{}' passed to --data-dir does not exist.".format(data_dir)
        logger.fatal(msg)
        raise RuntimeError(msg)

    try:
        files = {"python": "analyze.py", "r": "analyze.R"}
        analysis_script = pkg_resources.resource_filename(
            "doppel", "bin/{}".format(files[language])
        )
    except KeyError:
        msg = "doppel does not know how to test {} packages".format(language)
        logger.fatal(msg)
        raise KeyError(msg)

    logger.info(analysis_script)

    cmd = (
        "{} --pkg {} --output_dir {} "
        "--kwargs-string ~~KWARGS~~ "
        "--constructor-string ~~CONSTRUCTOR~~"
    )
    cmd = cmd.format(analysis_script, pkg_name, data_dir)

    if verbose is True:
        cmd += " --verbose"

    logger.info("Describing package with command:\n {}".format(cmd))

    # Invoke the analysis script
    exit_code = os.system(cmd)

    if exit_code != 0:
        msg = "doppel-describe exited with non-zero exit code: {}".format(exit_code)
        logger.fatal(msg)
        raise RuntimeError(msg)

    return


if __name__ == "__main__":
    main()
