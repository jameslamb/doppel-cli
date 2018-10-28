# doppel

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

## Example: Testing continuity between R and Python implementations

In this example, I'll show how to use `doppel` to test continuity between R and Python implementations of the same API. For this example, I used the `argparse` library.

NOTE: This example assumes that you already have `argparse` installed locally. If you don't run one or both of these:

```{shell}
Rscript -e "install.packages('argparse')"
pip install argparse
```

First, you need to generate special files that `doppel` uses to store information about a project's API. These are created using the `doppel-describe` tool.


```{shell}
# The R package
doppel-describe -p argparse --language R --data-dir $(pwd)/test_data

# The python package
doppel-describe -p argparse --language python --data-dir $(pwd)/test_data
```

Cool! Let's do some testing! `doppel-test` can be used to compare multiple packages.

```{shell}
doppel-test \
    --files test_data/python_argparse.json,test_data/r_argparse.json
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


Class Count
===========
+---------------------+----------------+
|   argparse [python] |   argparse [r] |
+=====================+================+
|                   9 |              0 |
+---------------------+----------------+


Test Failures (1)
===================
1. Packages have different counts of exported classes! argparse [python] (9), argparse [r] (0)
```

As you can see above, the `argparse` Python package has 9 exported classes while the R package has none.

From `doppel`'s perspective, this is considered a test failure. If you run `echo $?` in the terminal, should should see `1` printed. Returning a non-zero exit code like this tells CI tools like [Travis](https://travis-ci.org/) that the test was a failure, making `doppel` useful for CI (more on this in a future example).

You may be thinking "well wait, surely you'd want to test for way more stuff than just counts of classes and functions, right?". Absolutely! See [doppel's issues]() for a backlog of features I'd like to add. PRs are welcomed!!!

# Design Principles

A `test_failure` always results in a non-zero exit code.

# Ideas

* Degree of similarity should be configurable
    * should be able to say "only functions"
    * should be able to say "only classes"
    * should be able to whitelist "extras" and have them not count against the final test
* Handling of language-specific features
    * constructor names
    * kwargs
    * active bindings (R)
    * magic methods (Python)
    * S3 methods (R)
* should handle within-package inheritance in classes
* should handle cross-package inheritance with classes
* should have its own reliable CI (this will be fun to set up...)
* checks:
    * differing number of classes
    * differing number of functions
    * 'specific_function' exists in one but not other
    * 'specific class' exists in one but not other
    * differing number of public methods for 'specific_class'
    * 'specific_method' exists in one but not other
    * differing number of public members for class in one but not other
    * 'specific_member' exists in one but not other
    * different number of args for a particular function or method
    * 'specific_arg' is in the signature of 'specific_function_or_method' in one but not the other

# References

1. [Writing Command-Line tools with Click](https://dbader.org/blog/python-commandline-tools-with-click)
2. [Python entrypoints explained](https://amir.rachum.com/blog/2017/07/28/python-entry-points/)
