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

"""Stores information about the current work environment for use handling jobs.
"""

from __future__ import absolute_import, division, print_function

import rq

connection = None

def queue():
    """Creates a queue connected to the service that initiated the current job.

    Useful when a job handler needs to spawn additional jobs.

    Returns
    -------
    queue: :class:`rq.Queue`
        New queue pointing to the service where the current job originated.
    """
    if connection is None:
        raise RuntimeError("Cannot create a queue without a connection.  Are you running outside a worker?")
    return rq.Queue(connection=connection)
