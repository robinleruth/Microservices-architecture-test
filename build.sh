#!/bin/bash

pip install wheel

python3 common/setup.py bdist_wheel

cp -r dist users/dist
