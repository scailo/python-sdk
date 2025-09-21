#!/bin/bash

python build.py

rm -rf build
rm -rf dist

# cd scailo_sdk
python setup.py sdist bdist_wheel

# Upload to test.pypi.org
twine upload --repository testpypi dist/* --verbose
# Upload to pypi.org
twine upload dist/* --verbose

# pip install dist/scailo_sdk-0.1.2.tar.gz