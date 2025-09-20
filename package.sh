#!/bin/bash

cd scailo_sdk
python setup.py sdist bdist_wheel

# Upload to test.pypi.org
twine upload --repository testpypi dist/* --verbose
# Upload to pypi.org
twine upload dist/* --verbose