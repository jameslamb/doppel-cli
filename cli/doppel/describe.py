
import click
import pkg_resources
import os

@click.command()
@click.option(
    '--language', '-l',
    help="Programming language. Currently python and R are supported."
)
@click.option(
    '--pkg_name', '-p',
    help="Name of a package"
)
def main(language, pkg_name):
    """
    Generate a description of the public API for a software package.
    """
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
        raise KeyError("doppel does not know how to test {} pckages".format(language))

    output_dir = '/Users/jlamb/repos/doppel/more_tests'
    print(analysis_script)

    cmd = '{} --pkg {} --output_dir {}'.format(analysis_script, pkg_name, output_dir)

    print("Describing package with command:\n {}".format(cmd))
    # Invoke the analysis script
    os.system(cmd)

    return


if __name__ == "__main__":
    main()
