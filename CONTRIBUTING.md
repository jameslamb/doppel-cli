# Contribution Guidelines

This document contains information for maintainers and contributing developers. It has everything you need to know to make `doppel-cli` awesome.

#### Table of Contents

* [Integrations](#integrations)
    * [Appveyor](#appveyor)
    * [Codecov](#codecov)
    * [pep8speaks](#pepspeaks)
    * [readthedocs.io](#rtd)
    * [Travis CI](#travis)
* [Testing](#testing)
* [Documentation](#docs)
* [Releases](#releases)
    * [releasing to PyPi](#pypi)
    * [releasing to conda-forge](#conda)
* [References for Developers](#references)

## Integrations <a name="integrations"></a>

### Appveyor <a name="appveyor"></a>

[Appveyor](https://www.appveyor.com/) is used to perform CI tasks in Windows environments. Appveyor jobs are used to ensure that `doppel-cli` continues to work for Windows users.

configuration: [.appveyor.yml](https://github.com/jameslamb/doppel-cli/blob/main/.appveyor.yml)

### Codecov <a name="codecov"></a>

[https://codecov.io/](https://codecov.io/) is used to handle a variety of details related to the [code coverage](https://en.wikipedia.org/wiki/Code_coverage) of `doppel-cli`'s unit tests. This service handles details like hosting interactive reports with line-by-line coverage breakdown and telling GitHub whether or not to fail PR checks.

configuration: [.codecov.yml](https://github.com/jameslamb/doppel-cli/blob/main/.codecovs.yml)

### pep8speaks <a name="pepspeaks"></a>

[pep8speaks](https://github.com/OrkoHunter/pep8speaks) is a GitHub app that automatically checks every pull request on `doppel-cli` for compliance with this project's preferred style for Python code. The `pep8speaks` bot leaves comments on open PRs if any issues are found, recommending how they can be addressed.

configuration: [.pep8speaks.yml](https://github.com/jameslamb/doppel-cli/blob/main/.pep8speaks.yml)

### readthedocs <a name="rtd"></a>

[readthedocs](https://readthedocs.org/) is used for free creation and hosting of the documentation for `doppel-cli`. The documentation at https://doppel-cli.readthedocs.io/en/latest/index.html# is created automatically, for free, from the `main` branch of this repository.

configuration: [.readthedocs.yml](https://github.com/jameslamb/doppel-cli/blob/main/.readthedocs.yml)

### Travis <a name="travis"></a>

[Travis CI](https://travis-ci.org/) is used to perform CI tasks in Linux and Mac OS environments. This integration is the most important one for `doppel-cli`.

configuration: [.travis.yml](https://github.com/jameslamb/doppel-cli/blob/main/.travis.yml)

## Testing <a name="testing"></a>

### Finding bugs using smoke tests <a name="smokey"></a>

A set of smoke tests are available that you can use to help find bugs in `doppel-cli`.

To see if `doppel-cli` works for Python and R packages it has been shown to work for in the past, run

```
./smoke_tests/run.sh
```

To try running `doppel-cli` against all R packages installed on your system (in random order), run

```
./smoke_tests/all_r_packages.sh
```

If anything breaks, [create an issue](https://github.com/jameslamb/doppel-cli/issues) that includes the logs of the run and the results of running `Rscript -e 'sessionInfo()'`.

## Documentation <a name="docs"></a>

## Releases <a name="releases"></a>

### Releasing to PyPi <a name="pypi"></a>

PyPi is the official package manager used for distributing Python packages.

Releases to PyPi are done automatically by GitHub Actions whenever a new release is created on [the Releases page](https://github.com/jameslamb/doppel-cli/releases).

### Releasing to conda-forge <a name="conda"></a>

This package is released to `conda-forge` for all major Platforms and all minor versions of Python `3.5.0` and greater.

The recipe for the conda package is maintained at https://github.com/conda-forge/doppel-cli-feedstock. To release a new version to `conda-forge`.

1. [Release to PyPi first](#pypi)
2. Fork the [feedstock repo](https://github.com/conda-forge/doppel-cli-feedstock)
3. Update the recipe on your fork, using [grayskull](https://conda-forge.org/blog//2020/03/05/grayskull).

```shell
GITHUB_USER=jameslamb
./.ci/update-conda-recipe.sh ${GITHUB_USER}
```

4. Navigate to your fork of `doppel-cli-feedstock` and open a pull request into [the main feedstock repo](https://github.com/conda-forge/doppel-cli-feedstock).
5. Once that pull request is merged, the new version will get built and published on `conda-forge`!

## References for Developers <a name="references"></a>

* [Writing Command-Line tools with Click](https://dbader.org/blog/python-commandline-tools-with-click)
* [Python entrypoints explained](https://amir.rachum.com/blog/2017/07/28/python-entry-points/)
* [Testing on multiple operating systems with Travis](https://docs.travis-ci.com/user/multi-os/)
* [Building Python and R in one environment on Travis](https://www.augustguang.com/travis-ci-for-python-and-r/)
* [R packages available via conda](https://docs.anaconda.com/anaconda/packages/r-language-pkg-docs/)
* [networkx: example appveyor setup for python](https://github.com/networkx/networkx/blob/master/.appveyor.yml)
* [simple codecov Python example](https://github.com/codecov/example-python/blob/master/.travis.yml)
* [pytest fixtures](https://docs.pytest.org/en/latest/fixture.html)
* [inspecting builtins](https://docs.python.org/3/library/inspect.html#introspecting-callables-with-the-signature-object)
* [putting stuff on conda](https://conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs-skeleton.html)
* [defining conda meta.yml](https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html)
* [uploading to Anaconda.org](https://conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs-skeleton.html#id7)
* [putting a package in a specific channel](https://enterprise-docs.anaconda.com/en/latest/data-science-workflows/packages/upload.html)
* [using Anacodna repository](https://docs.anaconda.com/anaconda-repository/2.23/user/using/)
