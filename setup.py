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
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
        "Topic :: System :: Distributed Computing",
    ],
    description="Lightweight, flexible render farm based on RQ and Redis.",
    install_requires=[
        "arrow",
        "blessings",
        "redis",
        "rq",
    ],
    maintainer="Timothy M. Shead",
    maintainer_email="tim@shead-custom-design.gov",
    packages=find_packages(),
    project_urls={
        "Chat": "https://buildcat.zulipchat.com",
        "Coverage": "https://coveralls.io/r/shead-custom-design/buildcat",
        "Documentation": "https://buildcat.readthedocs.io",
        "Issue Tracker": "https://github.com/shead-custom-design/buildcat/issues",
        "Regression Tests": "https://travis-ci.org/shead-custom-design/buildcat",
        "Source": "https://github.com/shead-custom-design/buildcat",
    },
    scripts=[
        "bin/buildcat",
        ],
    url="https://buildcat.readthedocs.io",
    version=re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        open(
            "buildcat/__init__.py",
            "r").read(),
        re.M).group(1),
)
