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

"""Objects that support the directed acyclic graph used to define a process."""

from __future__ import absolute_import, division, print_function

import abc

import six

@six.add_metaclass(abc.ABCMeta)
class Node(object):
    """Abstract base class for all user specified :ref:`targets` and :ref:`actions`."""
    def __init__(self):
        pass

    def __repr__(self):
        return "buildcat.Node()"

