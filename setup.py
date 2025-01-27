# flake8: noqa

#!/usr/bin/env python

# Copyright 2016 DIANA-HEP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

NAME = "histogrammar"

MAJOR = 1
REVISION = 0
PATCH = 30
DEV = False
# NOTE: also update version at: README.rst

with open("requirements.txt") as f:
    REQUIREMENTS = f.read().splitlines()

VERSION = "{major}.{revision}.{patch}".format(
    major=MAJOR, revision=REVISION, patch=PATCH
)
FULL_VERSION = VERSION
if DEV:
    FULL_VERSION += ".dev"
    with open("requirements-test.txt") as f:
        REQUIREMENTS += f.read().splitlines()

# read the contents of abstract file
with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()


def write_version_py(filename: str = "histogrammar/version.py") -> None:
    """Write package version to version.py.

    This will ensure that the version in version.py is in sync with us.

    :param filename: The version.py to write too.
    :type filename: str
    """
    # Do not modify the indentation of version_str!
    version_str = """\"\"\"THIS FILE IS AUTO-GENERATED BY SETUP.PY.\"\"\"

import re

name = \"{name!s}\"
__version__ = \"{version!s}\"
version = \"{version!s}\"
full_version = \"{full_version!s}\"
release = {is_release!s}

version_info = tuple(re.split(r"[-\.]", __version__))
specification = ".".join(version_info[:2])


def compatible(serializedVersion):
    selfMajor, selfMinor = map(int, version_info[:2])
    otherMajor, otherMinor = map(int, re.split(r"[-\.]", serializedVersion)[:2])
    if selfMajor >= otherMajor:
        return True
    elif selfMinor >= otherMinor:
        return True
    else:
        return False
"""

    with open(filename, "w") as version_file:
        version_file.write(
            version_str.format(
                name=NAME.lower(),
                version=VERSION,
                full_version=FULL_VERSION,
                is_release=not DEV,
            )
        )


def setup_package() -> None:
    """The main setup method.

    It is responsible for setting up and installing the package.
    """
    write_version_py()

    setup(name=NAME,
          version=VERSION,
          packages=find_packages(),
          scripts=["scripts/hgwatch"],
          description="Composable histogram primitives for distributed data reduction.",
          long_description=long_description,
          long_description_content_type="text/x-rst",
          python_requires=">=3.6",
          author="Jim Pivarski (DIANA-HEP)",
          author_email="pivarski@fnal.gov",
          maintainer="Max Baak",
          maintainer_email="maxbaak@gmail.com",
          url="https://histogrammar.github.io/histogrammar-docs",
          download_url="https://github.com/histogrammar/histogrammar-python",
          license="Apache Software License v2",
          test_suite="tests",
          install_requires=REQUIREMENTS,
          classifiers=["Development Status :: 5 - Production/Stable",
                         "Environment :: Console",
                         "Intended Audience :: Science/Research",
                         "License :: OSI Approved :: Apache Software License",
                         "Topic :: Scientific/Engineering :: Information Analysis",
                         "Topic :: Scientific/Engineering :: Mathematics",
                         "Topic :: Scientific/Engineering :: Physics",
                       ],
          # files to be shipped with the installation, under: popmon/popmon/
          # after installation, these can be found with the functions in resources.py
          package_data=dict(
              histogrammar=[
                  "test_data/*.csv.gz",
                  "test_data/*.json*",
                  "notebooks/*tutorial*.ipynb",
              ]
          ),
          platforms="Any",
          )


if __name__ == "__main__":
    setup_package()
