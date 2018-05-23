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

"""Public API of Buildcat: an elegant, flexible, lightweight build system."""

from __future__ import absolute_import, division, print_function

import logging

from buildcat.action import *
from buildcat.build import *
from buildcat.process import *
from buildcat.target import *

__version__ = "0.1.0-dev"
"""Buildcat version, which follows the `Semantic Versioning <https://semver.org>`_ standard."""

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

