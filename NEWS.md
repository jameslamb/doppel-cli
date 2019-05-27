# doppel-cli

## development version

* Fixed bug which could cause `doppel-describe` to run endlessly in the presence of cyclic imports between submodules (e.g. in `pandas`). ([#120](https://github.com/jameslamb/doppel-cli/pull/120))
* Fixed bug which could cause a `ValueError` in `doppel-describe` when a Python package used CPython and had builtins that could not be inspected. This showed up in popular packages such as `pandas` and `numpy`. ([#94](https://github.com/jameslamb/doppel-cli/pull/94))

## 0.2.0

* `PackageCollection` will now reject lists of `packages` which have duplicated `name`s. This prevents some forms of silent failure. ([#110](https://github.com/jameslamb/doppel-cli/pull/110))
* `doppel-test` now checks for inconsistencies like "Public method 'bar()' on class 'Foo' exists in both packages but implementations have different order of keyword arguments" ([#108](https://github.com/jameslamb/doppel-cli/pull/108))
* Minor fixes to documentation ([#107](https://github.com/jameslamb/doppel-cli/pull/107))

## 0.1.8

* Python functions with decorators on them are now correctly handled by `doppel-describe` ([#99](https://github.com/jameslamb/doppel-cli/pull/99))
* Single-argument functions now have their arguments represented as `["arg"]` not `"arg"` in the JSON file produced by `doppel-describe`. ([#99](https://github.com/jameslamb/doppel-cli/pull/99))
* Added linting on `analyze.R` and removed dead code ([#93](https://github.com/jameslamb/doppel-cli/pull/93))
* Inherited class methods are now accurately handled using `doppel-describe` on Python packages. ([#97](https://github.com/jameslamb/doppel-cli/pull/97))
* `print()` on `R6` classes is now treated as a special method equivalent to `__str__()` in Python classes ([#97](https://github.com/jameslamb/doppel-cli/pull/97))
* The argument passed to `--kwargs-string` is now respected when describing the signature of R6 classes in `doppel-describe`. ([#97](https://github.com/jameslamb/doppel-cli/pull/97))
* function argument comparisons is now accurate and tested ([#89](https://github.com/jameslamb/doppel-cli/pull/89))
* `doppel-describe` no longer fails to parse packages which use callable classes as public methods ([#87](https://github.com/jameslamb/doppel-cli/pull/87))
* Failures in `doppel-describe` now result in a non-zero exit code. This was always the intended behavior, but was previously broken. ([#86](https://github.com/jameslamb/doppel-cli/pull/86))
* Check on whether on object belongs to a Python package or was imported is more accurate ([#85](https://github.com/jameslamb/doppel-cli/pull/85))
* Python packages with sub-modules no longer cause `doppel-describe` to hit an infinite recursion problem ([#73](https://github.com/jameslamb/doppel-cli/pull/73))

## 0.1.7

* Added constructors to list of public methods for both python and R ([#65](https://github.com/jameslamb/doppel-cli/pull/65))
* Added support for class methods in R6 ([#63](https://github.com/jameslamb/doppel-cli/pull/63))
* Fixed bug with empty R6 classes being excluded in `analyze.R` ([#62](https://github.com/jameslamb/doppel-cli/pull/62))
* Added checks on keyword arguments of public methods ([#58](https://github.com/jameslamb/doppel-cli/pull/58))

## 0.1.6

* Added ability to compare class methods across classes shared in all packages ([#40](https://github.com/jameslamb/doppel-cli/pull/40))
