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

import six

log = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class Criteria(object):
    def __init__(self):
        pass

    def __repr__(self):
        return "buildcat.build.Criteria()"

    @abc.abstractmethod
    def outdated(self, environment, inputs, outputs):
        raise NotImplementedError()


class Always(Criteria):
    def __init__(self):
        super(Always, self).__init__()

    def __repr__(self):
        return "buildcat.build.Always()"

    def outdated(self, environment, inputs, outputs):
        return True


class Never(Criteria):
    def __init__(self):
        super(Never, self).__init__()

    def __repr__(self):
        return "buildcat.build.Never()"

    def outdated(self, environment, inputs, outputs):
        return False


class Nonexistent(Criteria):
    def __init__(self):
        super(Nonexistent, self).__init__()

    def __repr__(self):
        return "buildcat.build.Nonexistent()"

    def outdated(self, environment, inputs, outputs):
        for node in outputs:
            if not node.exists(environment):
                return True
        return False
