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

"""Functionality for testing the buildcat installation and setup.
"""

from __future__ import absolute_import, division, print_function

import rq

import buildcat

def log(message):
    """Log a message.

    Parameters
    ----------
    message: str, required
        The message to be logged.
    """
    buildcat.log.info(message)

def spawn(count):
    """Create additional jobs.

    Parameters
    ----------
    count: int, required
        Number of new jobs to create.
    """
    for index in range(count):
        rq.Queue(connection=rq.get_current_connection()).enqueue("buildcat.test.log", "Job-{}".format(index))

def raise_exception(e):
    """Raise an exception.

    Useful for testing the reliability of workers.

    Parameters
    ----------
    e: exception object, required
        The exception to be raised.
    """
    raise e

