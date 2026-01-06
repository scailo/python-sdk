#!/bin/bash

.venv/bin/python build.py

rm -rf build
rm -rf dist

# cd scailo_sdk
.venv/bin/python setup.py sdist bdist_wheel

# Upload to test.pypi.org
.venv/bin/twine upload --repository testpypi dist/* --verbose
# Upload to pypi.org
.venv/bin/twine upload dist/* --verbose

# pip install dist/scailo_sdk-0.1.2.tar.gz