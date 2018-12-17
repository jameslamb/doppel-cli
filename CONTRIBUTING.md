# Contribution Guidelines

This document contains information necessary to contribute to this project. It includes some information describing tasks to be carried out exclusively by the maintainer.

## Testing releases: test PyPi

PyPi is the official package manage used for distributing Python packages. A "test" version is provided for side effect free integration testing.

To test whether the current state of publishing `doppel` plays nicely with PyPi, maintainers may from time to time run the following:

```
./test_publish.sh
```
