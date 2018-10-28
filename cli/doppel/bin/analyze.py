#!/usr/bin/env python3

import argparse
import inspect
import json
import os
import types

parser = argparse.ArgumentParser()
parser.add_argument(
    "--pkg"
    , type=str
    , help="Name of the python package to test"
)
parser.add_argument(
   "--output_dir"
   , type=str
   , default=os.getcwd()
   , help="Path to write files to"
)

# Grab args (store in constants for easier debugging)
args = parser.parse_args()
PKG_NAME = args.pkg
OUT_DIR = args.output_dir
LANGUAGE = 'python'

# Import that module
top_level_env = __import__(PKG_NAME)

# Set up the thing
out = {
    "name": "{} [python]".format(PKG_NAME),
    "language": "python",
    "functions": {},
    "classes": {}
}

# lil helper
def _log_info(msg):
    print(msg)

modules_to_parse = [top_level_env]

while len(modules_to_parse) > 0:

    # Grab the next module
    pkg_env = modules_to_parse.pop()

    # Get the exported stuff
    export_names = list(filter(lambda x: not x.startswith('_'), dir(pkg_env)))

    for obj_name in export_names:
        # Grab the object
        obj = getattr(pkg_env, obj_name)
        # Is it a function?
        if isinstance(obj, types.FunctionType):
            out["functions"][obj_name] = []
            next
        # Is it a class?
        elif inspect.isclass(obj):
            # Is it an exception? (skip)
            if issubclass(obj, Exception):
                _log_info("{} is an Exception. Skipping.".format(obj_name))
            else:
                out['classes'][obj_name] = []
            next
        elif isinstance(obj, types.ModuleType):
            _log_info("{} is a module".format(obj_name))
            modules_to_parse.append(obj)
        else:
            _log_info("Could not figure out what {} is".format(obj_name))

# write it out
out_file = os.path.join(OUT_DIR, "{}_{}.json".format(LANGUAGE, PKG_NAME))
_log_info("Writing output to {}".format(PKG_NAME))
with open(out_file, 'w') as f:
    f.write(json.dumps(out))
_log_info("Done analyzing this package.")
