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

from __future__ import absolute_import, division, print_function

import logging
import os

import buildcat.node

log = logging.getLogger(__name__)


class Target(buildcat.node.Node):
    def __init__(self, label):
        super(Target, self).__init__(label)

    def __repr__(self):
        return "buildcat.target.Target(label=%r)" % self._label

    def exists(self, environment):
        return False


class Directory(Target):
    def __init__(self, path, label=None):
        if label is None:
            label = path
        super(Directory, self).__init__(label)
        self._path = path

    def __repr__(self):
        return "buildcat.target.Directory(label=%r, path=%r)" % (self._label, self._path)

    @property
    def path(self):
        return self._path

    def exists(self, environment):
        path = environment.abspath(self._path)
        return os.path.isdir(path)

    def string(self, environment):
        return environment.abspath(self._path)


class File(Target):
    def __init__(self, path, label=None):
        if label is None:
            label = path
        super(File, self).__init__(label)
        self._path = path

    def __repr__(self):
        return "buildcat.target.File(label=%r, path=%r)" % (self._label, self._path)

    @property
    def path(self):
        return self._path

    def exists(self, environment):
        path = environment.abspath(self._path)
        return os.path.exists(path)

    def string(self, environment):
        return environment.abspath(self._path)

