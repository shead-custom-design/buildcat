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

import abc
import logging
import os

import buildcat.node

log = logging.getLogger(__name__)


class Target(buildcat.node.Node):
    def __init__(self):
        super(Target, self).__init__()

    def __repr__(self):
        return "buildcat.target.Target()"

    @abc.abstractmethod
    def exists(self, environment):
        return False

    @abc.abstractmethod
    def timestamp(self, environment):
        return None


class Directory(Target):
    def __init__(self, path):
        super(Directory, self).__init__()
        self._path = path

    def __repr__(self):
        return "buildcat.target.Directory(path=%r)" % (self._path)

    def exists(self, environment):
        return os.path.isdir(environment.abspath(self._path))

    def timestamp(self, environment):
        try:
            return os.path.getmtime(environment.abspath(self._path))
        except:
            return None

    @property
    def path(self):
        return self._path

    def string(self, environment):
        return environment.abspath(self._path)


class File(Target):
    def __init__(self, path):
        super(File, self).__init__()
        self._path = path

    def __repr__(self):
        return "buildcat.target.File(path=%r)" % (self._path)

    def exists(self, environment):
        return os.path.exists(environment.abspath(self._path))

    def timestamp(self, environment):
        try:
            return os.path.getmtime(environment.abspath(self._path))
        except:
            return None

    @property
    def path(self):
        return self._path

    def string(self, environment):
        return environment.abspath(self._path)

