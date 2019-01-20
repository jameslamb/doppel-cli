# Contribution Guidelines

This document contains information for maintainers and contributing developers. It has everything you need to know to make `doppel-cli` awesome.

#### Table of Contents

* [Integrations](#integrations)
    * Appveyor
    * readthedocs.io
    * Travis CI
* [Testing](#testing)
* [Documentation](#docs)
* [Releases](#releases)
* [References for Developers](#references)

## Integrations <a name="integrations"></a>

## Testing <a name="testing"></a>

## Documentation <a name="documentation"></a>

## Releases <a name="releases"></a>

### Testing releases: test PyPi

PyPi is the official package manage used for distributing Python packages. A "test" version is provided for side effect free integration testing.

To test whether the current state of publishing `doppel` plays nicely with PyPi, maintainers may from time to time run the following:

```
./publish.sh testpypi
```

To actually publish a new version, run:

```
./publish.sh pypi
```

## References for Developers <a name="references"></a>

1. [Writing Command-Line tools with Click](https://dbader.org/blog/python-commandline-tools-with-click)
2. [Python entrypoints explained](https://amir.rachum.com/blog/2017/07/28/python-entry-points/)
3. [Testing on multiple operating systems with Travis](https://docs.travis-ci.com/user/multi-os/)
4. [Building Python and R in one environment on Travis](https://www.augustguang.com/travis-ci-for-python-and-r/)
5. [R packages available via conda](https://docs.anaconda.com/anaconda/packages/r-language-pkg-docs/)
6. [networkx: example appveyor setup for python](https://github.com/networkx/networkx/blob/master/.appveyor.yml)
