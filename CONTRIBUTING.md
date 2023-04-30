# Contribution Guidelines

This document contains information for maintainers and contributing developers. It has everything you need to know to make `doppel-cli` awesome.

#### Table of Contents

* [Integrations](#integrations)
    * [GitHub Actions](#gha)
    * [readthedocs.io](#rtd)
* [Testing](#testing)
* [Documentation](#docs)
* [Releases](#releases)
    * [releasing to PyPi](#pypi)
    * [releasing to conda-forge](#conda)
* [References for Developers](#references)

## Integrations <a name="integrations"></a>

### GitHub Actions <a name="gha"></a>

[GitHub Actions](https://github.com/features/actions) is used to perform CI tasks in Linux and Mac OS environments. This integration is the most important one for `doppel-cli`.

configuration: [.github/workflows/ci.yml](https://github.com/jameslamb/doppel-cli/blob/main/.github/workflows/ci.yml)

### readthedocs <a name="rtd"></a>

[readthedocs](https://readthedocs.org/) is used for free creation and hosting of the documentation for `doppel-cli`. The documentation at https://doppel-cli.readthedocs.io/en/latest/index.html# is created automatically, for free, from the `main` branch of this repository.

configuration: [.readthedocs.yml](https://github.com/jameslamb/doppel-cli/blob/main/.readthedocs.yml)

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

The recipe for the conda package is maintained at https://github.com/conda-forge/doppel-cli-feedstock.

Within a few hours of a new release to PyPI, `conda-forge`'s automation creates a pull request in that repo.

To release a new version to `conda-forge`, just merge that PR.
