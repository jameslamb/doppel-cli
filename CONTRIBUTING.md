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
    * [releasing to Anaconda Cloud](#conda)
* [References for Developers](#references)

## Integrations <a name="integrations"></a>

### Appveyor <a name="appveyor"></a>

[Appveyor](https://www.appveyor.com/) is used to perform CI tasks in Windows environments. Appveyor jobs are used to ensure that `doppel-cli` continues to work for Windows users.

configuration: [.appveyor.yml](https://github.com/jameslamb/doppel-cli/blob/master/.appveyor.yml)

### Codecov <a name="codecov"></a>

[https://codecov.io/](https://codecov.io/) is used to handle a variety of details related to the [code coverage](https://en.wikipedia.org/wiki/Code_coverage) of `doppel-cli`'s unit tests. This service handles details like hosting interactive reports with line-by-line coverage breakdown and telling GitHub whether or not to fail PR checks.

configuration: [.codecov.yml](https://github.com/jameslamb/doppel-cli/blob/master/.codecovs.yml)

### pep8speaks <a name="pepspeaks"></a>

[pep8speaks](https://github.com/OrkoHunter/pep8speaks) is a GitHub app that automatically checks every pull request on `doppel-cli` for compliance with this project's preferred style for Python code. The `pep8speaks` bot leaves comments on open PRs if any issues are found, recommending how they can be addressed.

configuration: [.pep8speaks.yml](https://github.com/jameslamb/doppel-cli/blob/master/.pep8speaks.yml)

### readthedocs <a name="rtd"></a>

[readthedocs](https://readthedocs.org/) is used for free creation and hosting of the documentation for `doppel-cli`. The documentation at https://doppel-cli.readthedocs.io/en/latest/index.html# is created automatically, for free, from the `master` branch of this repository.

configuration: [.readthedocs.yml](https://github.com/jameslamb/doppel-cli/blob/master/.readthedocs.yml)

### Travis <a name="travis"></a>

[Travis CI](https://travis-ci.org/) is used to perform CI tasks in Linux and Mac OS environments. This integration is the most important one for `doppel-cli`.

configuration: [.travis.yml](https://github.com/jameslamb/doppel-cli/blob/master/.travis.yml)

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

PyPi is the official package manager used for distributing Python packages. A "test" version is provided for side effect free integration testing.

To test whether the current state of publishing `doppel` plays nicely with PyPi, maintainers may from time to time run the following:

```
./publish.sh testpypi
open https://test.pypi.org/project/doppel-cli/
```

To actually publish a new version, run:

```
./publish.sh pypi
open https://pypi.org/project/doppel-cli/
```

### Releasing to Anaconda Cloud <a name="conda"></a>

This package is released to Anaconda Cloud for all major Platforms and all minor versions of Python `3.5.0` and greater.

The recipe for building the package can be found in `conda-recipe/`, and was created using [this tutorial](https://conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs-skeleton.html).

To build packages for upload, you will need `conda-build`. It can be installed with

```
conda install -y conda-build
```

To build for all platforms, run

```

```

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
