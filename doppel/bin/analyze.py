#!/usr/bin/env python3

import argparse
import inspect
import json
import os
import sys
import types
import re


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pkg",
        type=str,
        help="Name of the python package to test"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=os.getcwd(),
        help="Path to write files to"
    )
    parser.add_argument(
        "--kwargs-string",
        type=str,
        help="String value to replace **kwarg"
    )
    parser.add_argument(
        "--constructor-string",
        type=str,
        help="String value to replace the constructor in the list of class public methods"
    )
    return(parser.parse_args(args))


def do_everything(parsed_args):

    # Grab args (store in constants for easier debugging)
    PKG_NAME = parsed_args.pkg
    OUT_DIR = parsed_args.output_dir
    KWARGS_STRING = parsed_args.kwargs_string
    CONSTRUCTOR_STRING = parsed_args.constructor_string
    LANGUAGE = 'python'

    # These are lanaguage-specific
    # conventions we can drop
    SPECIAL_METHOD_ARGS = [
        'self',
        'cls'
    ]

    # value to use for an empty function
    EMPTY_FUNCTION_DICT = {
        "args": []
    }

    # Import that module
    top_level_env = __import__(PKG_NAME)

    # Set up the thing
    out = {
        "name": "{} [python]".format(PKG_NAME),
        "language": "python",
        "functions": {},
        "classes": {}
    }

    def _log_info(msg):
        print(msg)

    def _log_warn(msg):
        print("[WARN] " + msg)

    def _get_arg_names(f, kwargs_string):
        """
        Given a function object, get its argument names.
        """
        f_dict = inspect.getfullargspec(f)._asdict()
        args = f_dict['args'] + f_dict['kwonlyargs']
        # deal with people passing "**kwargs"
        if f_dict['varkw'] is not None:
            args.append(kwargs_string)
        return(args)

    def _remove_decorators(thing):
        """
        Given a python object instrumented with one
        or more decorators, keep removing decorators
        until you get to the base object
        """
        if not hasattr(thing, '__wrapped__'):
            return(thing)
        else:
            msg = "'{}' is decorated, grabbing the underlying object"
            _log_info(msg.format(f))
            return(_remove_decorators(thing.__wrapped__))

    modules_to_parse = [top_level_env]
    names_of_parsed_modules = set([])

    while len(modules_to_parse) > 0:

        # Grab the next module
        pkg_env = modules_to_parse.pop()

        # Add it to the list of "modules we've already seen"
        names_of_parsed_modules.add(pkg_env.__name__)

        # Get the exported stuff
        export_names = list(filter(
            lambda x: not x.startswith('_'),
            dir(pkg_env)
        ))

        for obj_name in export_names:

            # Grab the object
            obj = getattr(pkg_env, obj_name)
            obj = _remove_decorators(obj)

            # Is it a function?
            if isinstance(obj, types.FunctionType):

                # Handle special cases where someone did
                # "from <pkg> import <whatever>" in a module.
                #
                # So, for example, "from requests import get"
                # would make it look like an object "get" is in
                # the namespace of your package. However, get.__module__
                # holds the fully-qualified name that tells you it's from
                # requests
                #
                if obj.__module__.startswith(PKG_NAME):
                    _log_info("'{}' is a function in this package, adding it".format(obj_name))
                    out["functions"][obj_name] = {
                        "args": _get_arg_names(obj, kwargs_string=KWARGS_STRING)
                    }

                next

            # Is it a class?
            elif inspect.isclass(obj):
                # Is it an exception? (skip)
                if issubclass(obj, Exception):
                    _log_info("{} is an Exception. Skipping.".format(obj_name))
                else:
                    # imports like 'from requests.adapter import HTTPAdapter'
                    regex = "'" + PKG_NAME + "\\.+.*"
                    is_in_package = bool(re.search(regex, str(obj)))

                    if is_in_package:
                        _log_info("'{}' is a class in this package, adding it".format(obj_name))
                        out['classes'][obj_name] = {}
                        out['classes'][obj_name]['public_methods'] = {}

                        for f in dir(obj):

                            # If attribute is internal, move on.
                            # This short-circuiting is nice to also avoid having to deal
                            # with custom stuff like read-only descriptors
                            # e.g. https://stackoverflow.com/a/24914634
                            is_private = f.startswith("_")
                            is_constructor = f == '__init__'
                            if is_private and not is_constructor:
                                continue

                            # Check characteristics of this attribute
                            class_member = getattr(obj, f)
                            class_member = _remove_decorators(class_member)
                            is_function = isinstance(class_member, types.FunctionType)

                            # Class methods are technically classes, types.FunctionType()
                            # yields false. But we want to treat them as public methods of
                            # a parent class here
                            # h/t https://stackoverflow.com/a/31843829 on the solution
                            is_class_method = False
                            if not is_function:
                                try:
                                    is_class_method = str(obj) == str(class_member.__self__)
                                    _log_info("'" + f + "' is a class method")
                                except AttributeError:
                                    pass

                            # If ClassA has a class ClassB as a public member,
                            # ClassB is basically being used like a public method. Treat it
                            # like that and grab the arguments of its constructor
                            if is_class_method or inspect.isclass(class_member):
                                class_member = class_member.__init__
                                is_function = True

                            if is_function or is_class_method:

                                # Try figuring out the actual signature, to see if
                                # we hit the "no signature found for built-in" error
                                # details: https://docs.python.org/3/library/inspect.html#introspecting-callables-with-the-signature-object
                                try:
                                    res = inspect.signature(class_member)
                                    method_args = _get_arg_names(
                                        class_member,
                                        KWARGS_STRING
                                    )
                                except ValueError:
                                    msg = "Could not figure out signature of builtin {}".format(
                                        class_member.__qualname__
                                    )
                                    _log_warn(msg)
                                    method_args = []

                                # Handle Python "self" conventions
                                method_args = [
                                    a for a in method_args if a not in SPECIAL_METHOD_ARGS
                                ]

                                # If we're dealing with the class constructor, use the
                                # passed-in replacement value
                                if is_constructor:
                                    f = CONSTRUCTOR_STRING

                                out['classes'][obj_name]['public_methods'][f] = {
                                    "args": method_args
                                }

                        # classes that don't implement a constructor
                        # still have one!
                        if not out['classes'][obj_name]['public_methods'].get(CONSTRUCTOR_STRING, None):
                            msg = "Class '{}' did not implement __init__. Adding it".format(obj_name)
                            _log_info(msg)

                            out['classes'][obj_name]['public_methods'][CONSTRUCTOR_STRING] = EMPTY_FUNCTION_DICT

                next

            elif isinstance(obj, types.ModuleType):
                _log_info("{} is a module".format(obj_name))

                # If the module isn't defined inside this package, ignore it.
                # Otherwise, it must be a sub-package we need to explore
                exact_match = obj.__package__ == PKG_NAME
                looks_like_submodule = obj.__name__.startswith(PKG_NAME + '.')

                is_in_package = exact_match or looks_like_submodule
                if is_in_package:

                    # Some importing strategies can make it seem like the package
                    # has a sub-module exactly named the same as the package, which
                    # can cause an infinite recursion problem. Skip it when that happens
                    if obj.__name__ == PKG_NAME:
                        _log_info("Skipping module '{}'".format(obj.__name__))
                    else:
                        if obj.__name__ in names_of_parsed_modules:
                            _log_info("Module '{}' is in this package but has already been parsed.".format(obj.__name__))
                        else:
                            _log_info("Module '{}' is in this package, adding it.".format(obj.__name__))
                            modules_to_parse.append(obj)
            else:
                _log_info("Could not figure out what {} is".format(obj_name))

    # write it out
    out_file = os.path.join(OUT_DIR, "{}_{}.json".format(LANGUAGE, PKG_NAME))
    _log_info("Writing output to {}".format(PKG_NAME))
    with open(out_file, 'w') as f:
        f.write(json.dumps(out))
    _log_info("Done analyzing this package.")


# Structuring things like this so it can be instrumented
# for test coverage.
# See https://stackoverflow.com/a/18161115 for more
if __name__ == "__main__":

    parsed_args = parse_args(sys.argv[1:])
    do_everything(parsed_args)
