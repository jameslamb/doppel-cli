#!/bin/sh
cd $TRAVIS_BUILD_DIR/tests
python3 -m unittest
