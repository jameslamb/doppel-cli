# doppel

[![Travis Build Status](https://travis-ci.org/jameslamb/doppel.svg?branch=master)](https://travis-ci.org/jameslamb/doppel)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/github/jameslamb/doppel?branch=master&svg=true)](https://ci.appveyor.com/project/jameslamb/doppel)
[![Python Versions](https://img.shields.io/pypi/pyversions/doppel-cli.svg)](https://pypi.org/project/doppel-cli)
[![PyPI Version](https://img.shields.io/pypi/v/doppel-cli.svg)](https://pypi.org/project/doppel-cli)

`doppel` is an integration testing framework for testing API similarity across languages.

# What is the value of keeping the same public interface?

This project tests API consistency in libraries across languages.

Why is this valuable?

* For developers:
    * less communication overhead implementing changes across languages
    * forcing function to limit growth in complexity of the public API
* For users:
    * no need to re-learn the API when switching languages
    * form better expectations when switching languages

## Getting started

`doppel` can be installed from source just like any other python package.

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

# Ideas

* Degree of similarity should be configurable
    * should be able to say "only functions"
    * should be able to say "only classes"
    * should be able to whitelist "extras" and have them not count against the final test
* Handling of language-specific features
    * constructor names
    * magic methods (Python)
    * S3 methods (R)
* should handle within-package inheritance in classes
* should handle cross-package inheritance with classes
* checks:
    * differing number of public methods for 'specific_class'
    * 'specific_method' exists in one but not other
    * differing number of public members for class in one but not other
    * 'specific_member' exists in one but not other
    * different number of args for a particular function or method
    * 'specific_arg' is in the signature of 'specific_function_or_method' in one but not the other

# References

1. [Writing Command-Line tools with Click](https://dbader.org/blog/python-commandline-tools-with-click)
2. [Python entrypoints explained](https://amir.rachum.com/blog/2017/07/28/python-entry-points/)
3. [Testing on multiple operating systems with Travis](https://docs.travis-ci.com/user/multi-os/)
4. [Building Python and R in one environment on Travis](https://www.augustguang.com/travis-ci-for-python-and-r/)
5. [R packages available via conda](https://docs.anaconda.com/anaconda/packages/r-language-pkg-docs/)
6. [networkx: example appveyor setup for python](https://github.com/networkx/networkx/blob/master/.appveyor.yml)
