#!/usr/bin/env python3

import argparse
import inspect
import json
import logging
import os
import sys
import types
import re

logger = logging.getLogger()
logging.basicConfig(
    format='%(levelname)s [%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout
)


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
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Use this flag to get more detailed logs"
    )
    return(parser.parse_args(args))


def do_everything(parsed_args):

    # Grab args (store in constants for easier debugging)
    PKG_NAME = parsed_args.pkg
    OUT_DIR = parsed_args.output_dir
    KWARGS_STRING = parsed_args.kwargs_string
    CONSTRUCTOR_STRING = parsed_args.constructor_string

    VERBOSE = parsed_args.verbose
    if VERBOSE is True:
        logger.setLevel(logging.DEBUG)
        logger.debug("Running doppel-describe with verbose logging.")
    else:
        logger.setLevel(logging.INFO)

    LANGUAGE = 'python'

    # Other repeated constants
    ARGS_KEY = "args"
    CLASSES_KEY = "classes"
    FUNCTIONS_KEY = "functions"
    PUBLIC_METHODS_KEY = "public_methods"

    # These are lanaguage-specific
    # conventions we can drop
    SELF_KEYWORD = 'self'
    CLASS_KEYWORD = 'cls'
    SPECIAL_METHOD_ARGS = [
        SELF_KEYWORD,
        CLASS_KEYWORD
    ]

    # value to use for an empty function
    EMPTY_FUNCTION_DICT = {
        ARGS_KEY: []
    }

    # Import that module
    top_level_env = __import__(PKG_NAME)

    # Set up the thing
    out = {
        "name": "{} [python]".format(PKG_NAME),
        "language": "python",
        FUNCTIONS_KEY: {},
        CLASSES_KEY: {}
    }

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
            logger.info(msg.format(thing.__name__))
            return(_remove_decorators(thing.__wrapped__))

    def _is_builtin(obj):
        """
        Checks whether an object is a built-in,
        such as 'min()'.
        """
        return str(obj).startswith('<built-in ')

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
                    logger.info("'{}' is a function in this package, adding it".format(obj_name))
                    out[FUNCTIONS_KEY][obj_name] = {
                        ARGS_KEY: _get_arg_names(obj, kwargs_string=KWARGS_STRING)
                    }

                next

            # Is it a class?
            elif inspect.isclass(obj):
                # Is it an exception? (skip)
                if issubclass(obj, Exception):
                    logger.info("{} is an Exception. Skipping.".format(obj_name))
                else:
                    # imports like 'from requests.adapter import HTTPAdapter'
                    regex = "'" + PKG_NAME + "\\.+.*"
                    is_in_package = bool(re.search(regex, str(obj)))

                    if is_in_package:
                        logger.info("'{}' is a class in this package, adding it".format(obj_name))
                        out[CLASSES_KEY][obj_name] = {}
                        out[CLASSES_KEY][obj_name][PUBLIC_METHODS_KEY] = {}

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

                            # class members like a dictionary or string literal
                            # should not be included
                            if not callable(class_member):
                                continue

                            # built-ins like 'min()' need special handling
                            if _is_builtin(class_member):
                                msg = f"found built-in '{class_member.__name__}', could not get signature"
                                logger.warning(msg)
                                method_args = []
                                out[CLASSES_KEY][obj_name][PUBLIC_METHODS_KEY][f] = {
                                    ARGS_KEY: method_args
                                }
                                continue

                            # Class methods are technically classes, types.FunctionType()
                            # yields false. But we want to treat them as public methods of
                            # a parent class here
                            # h/t https://stackoverflow.com/a/31843829 on the solution
                            #
                            # If ClassA has a class ClassB as a public member,
                            # ClassB is basically being used like a public method. Treat it
                            # like that and grab the arguments of its constructor
                            #
                            is_class_method = str(getattr(class_member, '__self__', None)) == str(obj)
                            if not is_function and not is_constructor and not is_class_method:
                                init_args = _get_arg_names(
                                    class_member.__init__,
                                    KWARGS_STRING
                                )
                                is_class_method = (CLASS_KEYWORD in init_args) or (SELF_KEYWORD in init_args)
                                if is_class_method:
                                    class_member = class_member.__init__
                                    is_function = True
                                    logger.debug("'" + f + "' is a class method")

                            # Try figuring out the actual signature, to see if
                            # we hit the "no signature found for built-in" error
                            # details: https://docs.python.org/3/library/inspect.html#introspecting-callables-with-the-signature-object
                            #
                            # this is_function is still here to catch the case where the constructor
                            # wasn't implemented
                            if is_function or is_class_method:
                                method_args = _get_arg_names(
                                    class_member,
                                    KWARGS_STRING
                                )

                                # Handle Python "self" conventions
                                method_args = [
                                    a for a in method_args if a not in SPECIAL_METHOD_ARGS
                                ]

                                # If we're dealing with the class constructor, use the
                                # passed-in replacement value
                                if is_constructor:
                                    f = CONSTRUCTOR_STRING

                                out[CLASSES_KEY][obj_name][PUBLIC_METHODS_KEY][f] = {
                                    ARGS_KEY: method_args
                                }

                        # classes that don't implement a constructor
                        # still have one!
                        if not out[CLASSES_KEY][obj_name][PUBLIC_METHODS_KEY].get(CONSTRUCTOR_STRING, None):
                            msg = "Class '{}' did not implement __init__. Adding it".format(obj_name)
                            logger.info(msg)

                            out[CLASSES_KEY][obj_name][PUBLIC_METHODS_KEY][CONSTRUCTOR_STRING] = EMPTY_FUNCTION_DICT

                next

            elif isinstance(obj, types.ModuleType):
                logger.debug("{} is a module".format(obj_name))

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
                        logger.debug("Skipping module '{}'".format(obj.__name__))
                    else:
                        if obj.__name__ in names_of_parsed_modules:
                            logger.debug("Module '{}' is in this package but has already been parsed.".format(obj.__name__))
                        else:
                            logger.info("Module '{}' is in this package, adding it.".format(obj.__name__))
                            modules_to_parse.append(obj)

            # built-ins like 'min()' are not classes, functions, or modules,
            # according to the previous checks, but if they're callable
            # they should count as exported functions
            elif _is_builtin(obj) and callable(obj):
                if not obj.__module__.startswith(PKG_NAME):
                    logger.info("Callable '{}' is a built-in not included in this package's namespace. Skipping it.".format(obj.__name__))
                next

            else:
                logger.debug("Could not figure out what {} is".format(obj_name))

    # write it out
    out_file = os.path.join(OUT_DIR, "{}_{}.json".format(LANGUAGE, PKG_NAME))
    logger.info("Writing output to {}".format(PKG_NAME))
    with open(out_file, 'w') as f:
        f.write(json.dumps(out))
    logger.info("Done analyzing this package.")


# Structuring things like this so it can be instrumented
# for test coverage.
# See https://stackoverflow.com/a/18161115 for more
if __name__ == "__main__":  # pragma: no cover

    parsed_args = parse_args(sys.argv[1:])
    do_everything(parsed_args)
