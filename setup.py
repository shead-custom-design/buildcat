# Copyright 2018 Timothy M. Shead
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
import re

setup(
    author="Timothy M. Shead",
    author_email="tim@shead-custom-design.com",
    name="buildcat",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
        "Topic :: System :: Distributed Computing",
    ],
    description="Elegant, simple render farm based on rq.",
    install_requires=[
        "arrow",
        "blessings",
        "redis",
        "rq",
    ],
    maintainer_email="tim@shead-custom-design.gov",
    packages=["buildcat"],
    package_dir={"buildcat": "buildcat"},
    package_data={
        "buildcat": [
            "integrations/houdini/scd__buildcat.hdalc",
            "integrations/houdini/demo.hiplc",
            "integrations/modo/demo.lxo",
            ],
        },
    scripts=[
        "bin/buildcat",
        ],
    url="http://buildcat.readthedocs.org",
    version=re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        open(
            "buildcat/__init__.py",
            "r").read(),
        re.M).group(1),
)
