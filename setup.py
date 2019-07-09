# Copyright 2018 Timothy M. Shead
#
# This file is part of Buildcat.
#
# Buildcat is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Buildcat is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Buildcat.  If not, see <http://www.gnu.org/licenses/>.

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
            ],
        },
    scripts=[
        "bin/buildcat-install",
        ],
    url="http://buildcat.readthedocs.org",
    version=re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        open(
            "buildcat/__init__.py",
            "r").read(),
        re.M).group(1),
)
