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

"""Provides classes that represent ref:`targets` - artifacts to be created and/or updated by the build process."""

from __future__ import absolute_import, division, print_function

import abc
import logging
import os

import custom_inherit
import six

import buildcat.node

log = logging.getLogger(__name__)


@six.add_metaclass(custom_inherit.DocInheritMeta(abstract_base_class=True, style="numpy_napoleon"))
class Target(buildcat.node.Node):
    """Abstract base class for :ref:`targets` - artifacts that are used, created, or updated by the build process.

    Most build systems assume that a target is a file or directory located on a filesystem, and Buildcat provides
    :class:`buildcat.target.Directory` and :class:`buildcat.target.File` for this purpose; however, you are free to
    derive from :class:`buildcat.target.Target` to define your own target types - for example, you might define a target
    based on a record in a database, a resource accessed on a web server, or any other entity that could be used,
    created, or updated during the build.
    """
    def __init__(self):
        super(Target, self).__init__()

    def __repr__(self):
        return "buildcat.target.Target()"

    @abc.abstractmethod
    def exists(self, environment):
        """Return `True` if the target exists.

        Parameters
        ----------
        environment: :class:`buildcat.process.Environment`, required
            The current build environment.
        """
        return False

    @abc.abstractmethod
    def timestamp(self, environment):
        """Return the timestamp (number of seconds since the UNIX epoch) when the target was last created / modified.

        Parameters
        ----------
        environment: :class:`buildcat.process.Environment`, required
            The current build environment.
        """
        return None


class Directory(Target):
    """Buildcat :ref:`target <targets>` that represents a directory located on a filesystem.

    Parameters
    ----------
    path: str, required
        Absolute or relative path for this directory.  Note that relative paths are relative
        to the current working directory specified for the owning :class:`buildcat.process.Process`.
    """
    def __init__(self, path):
        super(Directory, self).__init__()
        self._path = path

    def __repr__(self):
        return "buildcat.target.Directory(path=%r)" % (self._path)

    @property
    def path(self):
        """str containing the unmodified absolute or relative directory path."""
        return self._path

    def exists(self, environment):
        """
        Returns
        -------
        exists: bool
            Returns `True` if the filesystem path exists and is a directory, otherwise `False`.
        """
        return os.path.isdir(environment.abspath(self._path))

    def timestamp(self, environment):
        try:
            return os.path.getmtime(environment.abspath(self._path))
        except:
            return None

    def string(self, environment):
        """String representation of the directory, for substitution into :class:`buildcat.action.Shell` commands."""
        return environment.abspath(self._path)


class File(Target):
    """Buildcat :ref:`target <targets>` that represents a file located on a filesystem.

    Parameters
    ----------
    path: str, required
        Absolute or relative path for this file.  Note that relative paths are relative
        to the current working directory specified for the owning :class:`buildcat.process.Process`.
    """
    def __init__(self, path):
        super(File, self).__init__()
        self._path = path

    def __repr__(self):
        return "buildcat.target.File(path=%r)" % (self._path)

    @property
    def path(self):
        """str containing the unmodified absolute or relative file path."""
        return self._path

    def exists(self, environment):
        """
        Returns
        -------
        exists: bool
            Returns `True` if the filesystem path exists and is a file, otherwise `False`.
        """
        return os.path.exists(environment.abspath(self._path))

    def timestamp(self, environment):
        try:
            return os.path.getmtime(environment.abspath(self._path))
        except:
            return None

    def string(self, environment):
        """String representation of the file, for substitution into :class:`buildcat.action.Shell` commands."""
        return environment.abspath(self._path)

