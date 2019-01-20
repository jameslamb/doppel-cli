# doppel-cli

[![Travis Build Status](https://travis-ci.org/jameslamb/doppel-cli.svg?branch=master)](https://travis-ci.org/jameslamb/doppel-cli)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/github/jameslamb/doppel-cli?branch=master&svg=true)](https://ci.appveyor.com/project/jameslamb/doppel-cli) [![Documentation Status](https://readthedocs.org/projects/doppel-cli/badge/?version=latest)](https://doppel-cli.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/jameslamb/doppel-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/jameslamb/doppel-cli) [![Python Versions](https://img.shields.io/pypi/pyversions/doppel-cli.svg)](https://pypi.org/project/doppel-cli) [![downloads](https://img.shields.io/pypi/dm/doppel-cli.svg)](https://pypi.org/project/doppel-cli) [![license](https://img.shields.io/pypi/l/doppel-cli.svg)](https://pypi.org/project/doppel-cli)

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

## Documentation

For the most up-to-date documentation, please see https://doppel-cli.readthedocs.io/en/latest/.

## Getting started

`doppel-cli` can be installed from source just like any other python package.

```
python setup.py install
```

You can also install from PyPi, the official package manage for Python. To avoid conflicts with the existing `doppel` project on that repository, it is distributed as `doppel-cli`.

```
pip install doppel-cli
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
    cat
```

This will yield something like this:

```{text}
Function Count
==============
+---------------------+----------------+
|   argparse [python] |   argparse [r] |
+=====================+================+
|                   1 |              1 |
+---------------------+----------------+


Function Names
==============
+-----------------+---------------------+----------------+
| function_name   | argparse [python]   | argparse [r]   |
+=================+=====================+================+
| ngettext        | yes                 | no             |
+-----------------+---------------------+----------------+
| ArgumentParser  | no                  | yes            |
+-----------------+---------------------+----------------+

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
| HelpFormatter                 | yes                 | no             |
+-------------------------------+---------------------+----------------+
| Namespace                     | yes                 | no             |
+-------------------------------+---------------------+----------------+
| RawDescriptionHelpFormatter   | yes                 | no             |
+-------------------------------+---------------------+----------------+
| ArgumentParser                | yes                 | no             |
+-------------------------------+---------------------+----------------+
| MetavarTypeHelpFormatter      | yes                 | no             |
+-------------------------------+---------------------+----------------+
| Action                        | yes                 | no             |
+-------------------------------+---------------------+----------------+
| ArgumentDefaultsHelpFormatter | yes                 | no             |
+-------------------------------+---------------------+----------------+
| FileType                      | yes                 | no             |
+-------------------------------+---------------------+----------------+
| RawTextHelpFormatter          | yes                 | no             |
+-------------------------------+---------------------+----------------+


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

You may be thinking "well wait, surely you'd want to test for way more stuff than just counts of classes and functions, right?". Absolutely! See [doppel's issues]() for a backlog of features I'd like to add. PRs are welcomed!!!

To learn more about the things that are currently configurable, you can run:

```
doppel-describe --help
```

and

```
doppel-test --help
```
