# doppel-cli

[![PyPI Version](https://img.shields.io/pypi/v/doppel-cli.svg)](https://pypi.org/project/doppel-cli) [![Travis Build Status](https://img.shields.io/travis/jameslamb/doppel-cli.svg?label=travis&logo=travis&branch=master)](https://travis-ci.org/jameslamb/doppel-cli)
[![AppVeyor Build Status](https://img.shields.io/appveyor/ci/jameslamb/doppel-cli.svg?label=appveyor&logo=appveyor&branch=master)](https://ci.appveyor.com/project/jameslamb/doppel-cli) [![Documentation Status](https://readthedocs.org/projects/doppel-cli/badge/?version=latest)](https://doppel-cli.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/jameslamb/doppel-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/jameslamb/doppel-cli) [![Python Versions](https://img.shields.io/pypi/pyversions/doppel-cli.svg)](https://pypi.org/project/doppel-cli) [![downloads](https://img.shields.io/pypi/dm/doppel-cli.svg)](https://pypi.org/project/doppel-cli) [![license](https://img.shields.io/pypi/l/doppel-cli.svg)](https://pypi.org/project/doppel-cli)

`doppel-cli` is an integration testing framework for testing API similarity across languages.

# What is the value of keeping the same public interface?

This project tests API consistency in libraries across languages.

Why is this valuable?

* For developers:
    * less communication overhead implementing changes across languages
    * forcing function to limit growth in complexity of the public API
* For users:
    * no need to re-learn the API when switching languages
    * form better expectations when switching languages

For more on this, click the link below to see this talk from the **satRdays Chicago 2019** conference:

[![satRdays Chicago](https://img.youtube.com/vi/quFhQvizBE8/0.jpg)](https://www.youtube.com/watch?v=quFhQvizBE8&t=2h24m30s)

## Documentation

For the most up-to-date documentation, please see https://doppel-cli.readthedocs.io/en/latest/.

## Getting started

`doppel-cli` can be installed from source just like any other python package.

```
python setup.py install
```

You can also install from PyPi, the official package manager for Python. To avoid conflicts with the existing `doppel` project on that repository, it is distributed as `doppel-cli`.

```
pip install doppel-cli
```

### R requirements

In order to use `doppel` on R packages, you will need the R packages shown in the following installation commands:

```{shell}
Rscript -e "
    install.packages(
        c('argparse', 'futile.logger', 'jsonlite', 'R6')
        , repos = 'http://cran.rstudio.com'
    )
"
```

## Example: Testing continuity between R and Python implementations

In this example, I'll show how to use `doppel` to test continuity between R and Python implementations of the same API. For this example, I used the `argparse` library.

NOTE: This example assumes that you already have `argparse` installed locally.

If you don't run one or both of these:

```{shell}
Rscript -e "install.packages('argparse')"
pip install argparse
```

First, you need to generate special files that `doppel` uses to store information about a project's API. These are created using the `doppel-describe` tool.

```{shell}
PACKAGE=argparse

# Create temporary directory to store output files
mkdir $(pwd)/test_data

# The R package
doppel-describe \
    -p ${PACKAGE} \
    --language R \
    --data-dir $(pwd)/test_data

# The python package
doppel-describe \
    -p ${PACKAGE} \
    --language python \
    --data-dir $(pwd)/test_data
```

Cool! Let's do some testing! `doppel-test` can be used to compare multiple packages.

```{shell}
doppel-test \
    --files $(pwd)/test_data/python_${PACKAGE}.json,$(pwd)/test_data/r_${PACKAGE}.json \
    | tee out.log \
    | cat
```

This will yield something like this:

```{text}
Function Count
==============
+---------------------+----------------+
|   argparse [python] |   argparse [r] |
+=====================+================+
|                   0 |              1 |
+---------------------+----------------+


Function Names
==============
+-----------------+---------------------+----------------+
| function_name   | argparse [python]   | argparse [r]   |
+=================+=====================+================+
| ArgumentParser  | no                  | yes            |
+-----------------+---------------------+----------------+

Function Argument Names
=======================
No shared functions.

Class Count
===========
+---------------------+----------------+
|   argparse [python] |   argparse [r] |
+=====================+================+
|                   9 |              0 |
+---------------------+----------------+


Class Names
===========
+-------------------------------+---------------------+----------------+
| class_name                    | argparse [python]   | argparse [r]   |
+===============================+=====================+================+
| MetavarTypeHelpFormatter      | yes                 | no             |
+-------------------------------+---------------------+----------------+
| ArgumentParser                | yes                 | no             |
+-------------------------------+---------------------+----------------+
| FileType                      | yes                 | no             |
+-------------------------------+---------------------+----------------+
| HelpFormatter                 | yes                 | no             |
+-------------------------------+---------------------+----------------+
| RawDescriptionHelpFormatter   | yes                 | no             |
+-------------------------------+---------------------+----------------+
| Action                        | yes                 | no             |
+-------------------------------+---------------------+----------------+
| ArgumentDefaultsHelpFormatter | yes                 | no             |
+-------------------------------+---------------------+----------------+
| Namespace                     | yes                 | no             |
+-------------------------------+---------------------+----------------+
| RawTextHelpFormatter          | yes                 | no             |
+-------------------------------+---------------------+----------------+


Class Public Methods
====================
No shared classes.

Arguments in Class Public Methods
=================================
No shared classes.

Test Failures (12)
===================
1. Function 'ngettext()' is not exported by all packages

2. Function 'ArgumentParser()' is not exported by all packages

3. Packages have different counts of exported classes! argparse [python] (9), argparse [r] (0)

4. Class 'HelpFormatter()' is not exported by all packages

5. Class 'Namespace()' is not exported by all packages

6. Class 'RawDescriptionHelpFormatter()' is not exported by all packages

7. Class 'ArgumentParser()' is not exported by all packages

8. Class 'MetavarTypeHelpFormatter()' is not exported by all packages

9. Class 'Action()' is not exported by all packages

10. Class 'ArgumentDefaultsHelpFormatter()' is not exported by all packages

11. Class 'FileType()' is not exported by all packages

12. Class 'RawTextHelpFormatter()' is not exported by all packages
```

As you can see above, the `argparse` Python package has 9 exported classes while the R package has none.

From `doppel`'s perspective, this is considered a test failure. If you run `echo $?` in the terminal, should should see `1` printed. Returning a non-zero exit code like this tells CI tools like [Travis](https://travis-ci.org/) that the test was a failure, making `doppel` useful for CI (more on this in a future example).

You may be thinking "well wait, surely you'd want to test for way more stuff than just counts of classes and functions, right?". Absolutely! See [the project issues issues](https://github.com/jameslamb/doppel-cli/issues) for a backlog of features I'd like to add. PRs are welcomed!!!

To learn more about the things that are currently configurable, you can run:

```
doppel-describe --help
```

and

```
doppel-test --help
```

## Contributing

Bug reports, questions, and feature requests should be directed to [the issues page](https://github.com/jameslamb/doppel-cli/issues).

See [CONTRIBUTING.md](./CONTRIBUTING.md) for information on how to contribute.
