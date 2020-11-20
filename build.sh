#!/bin/bash

pushd .
cd common
pip install wheel

python3 setup.py bdist_wheel

popd
cp -r common/dist users
cp -r common/dist event
