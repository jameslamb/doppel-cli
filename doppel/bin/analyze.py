#!/usr/bin/env python3

import argparse
import inspect
import json
import os
import types
import re

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

# Grab args (store in constants for easier debugging)
args = parser.parse_args()
PKG_NAME = args.pkg
OUT_DIR = args.output_dir
KWARGS_STRING = args.kwargs_string
CONSTRUCTOR_STRING = args.constructor_string
LANGUAGE = 'python'

# These are lanaguage-specific
# conventions we can drop
SPECIAL_METHOD_ARGS = [
    'self',
    'cls'
]

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


def _get_arg_names(f, kwargs_string):
    """
    Given a function object, get it's argument names.
    """
    f_dict = inspect.getfullargspec(f)._asdict()
    args = f_dict['args']
    # deal with people passing "**kwargs"
    if f_dict['varkw'] is not None:
        args.append(kwargs_string)
    return(args)


modules_to_parse = [top_level_env]

while len(modules_to_parse) > 0:

    # Grab the next module
    pkg_env = modules_to_parse.pop()

    # Get the exported stuff
    export_names = list(filter(
        lambda x: not x.startswith('_'),
        dir(pkg_env)
    ))

    for obj_name in export_names:

        # Grab the object
        obj = getattr(pkg_env, obj_name)

        # Is it a function?
        if isinstance(obj, types.FunctionType):

            # Handle special cases where someone did
            # "from <pkg> import <whatever>" in a module.
            if obj_name.startswith(PKG_NAME):
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

                    out['classes'][obj_name] = {}
                    out['classes'][obj_name]['public_methods'] = {}

                    for f in dir(obj):
                        func = getattr(obj, f)

                        is_callable = callable(func)
                        is_public = not f.startswith("_")
                        is_constructor = f == '__init__'
                        if is_callable and (is_public or is_constructor):

                            # Deal with decorators
                            try:
                                method_args = _get_arg_names(func, KWARGS_STRING)
                            except TypeError:
                                method_args = _get_arg_names(
                                    func.__wrapped__,
                                    KWARGS_STRING
                                )

                            # Handle Python "self" conventions
                            method_args = [
                                a for a in method_args if a not in SPECIAL_METHOD_ARGS
                            ]

                            # If we're dealing with the class constructor, use the
                            # passed-in replacement value
                            if f == '__init__':
                                f = CONSTRUCTOR_STRING

                            out['classes'][obj_name]['public_methods'][f] = {
                                "args": method_args
                            }
            next

        elif isinstance(obj, types.ModuleType):
            _log_info("{} is a module".format(obj_name))

            # If the module isn't defined inside this package, ignore it.
            # Otherwise, it must be a sub-package we need to explore
            regex = '.*[/]' + PKG_NAME + '[/]+.*'
            is_in_package = bool(re.search(regex, str(obj)))
            if is_in_package:
                modules_to_parse.append(obj)
        else:
            _log_info("Could not figure out what {} is".format(obj_name))

# write it out
out_file = os.path.join(OUT_DIR, "{}_{}.json".format(LANGUAGE, PKG_NAME))
_log_info("Writing output to {}".format(PKG_NAME))
with open(out_file, 'w') as f:
    f.write(json.dumps(out))
_log_info("Done analyzing this package.")
