
import click
import pkg_resources
import os
from sys import stdout


@click.command()
@click.option(
    '--language', '-l',
    help="Programming language. Currently python and R are supported."
)
@click.option(
    '--pkg_name', '-p',
    help="Name of a package"
)
@click.option(
    '--data-dir', '-d',
    help="Path to write output file to."
)
@click.option(
    '--version',
    default=False,
    help="Get the current version of doppel-describe",
    is_flag=True
)
def main(language: str, pkg_name: str, data_dir: str, version: bool) -> None:
    """
    Generate a description of the public API for a software package and
    write out a JSON representation of it.
    """
    if version is True:
        version_file = os.path.join(
            os.path.dirname(__file__),
            'VERSION'
        )
        with open(version_file, 'r') as f:
            out = f.read()
        stdout.write(out)
        return

    language = language.lower()
    print("Testing package {} [{}]".format(pkg_name, language))

    files = {
        'python': 'analyze.py',
        'r': 'analyze.R'
    }

    try:
        analysis_script = pkg_resources.resource_filename(
            'doppel', 'bin/{}'.format(files[language])
        )
    except KeyError:
        raise KeyError("doppel does not know how to test {} packages".format(language))

    print(analysis_script)

    cmd = '{} --pkg {} --output_dir {} --kwargs-string ~~KWARGS~~ --constructor-string ~~CONSTRUCTOR~~'.format(
        analysis_script, pkg_name, data_dir
    )

    print("Describing package with command:\n {}".format(cmd))

    # Invoke the analysis script
    exit_code = os.system(cmd)

    if exit_code != 0:
        msg = "doppel-describe exited with non-zero exit code: {}"
        raise RuntimeError(msg.format(exit_code))

    return


if __name__ == "__main__":
    main()
