# doppel

`doppel` is an integration testing framework for testing API similarity across languages.

# R example

Test a package

```{shell}
./analyze.R --pkg rsixygen --output_dir $(pwd)
```

Check out the output

```{shell}
cat rsixygen.json | jq .
```

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
