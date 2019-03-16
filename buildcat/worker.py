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

"""Custom RQ worker class for Windows portability.
"""

from __future__ import absolute_import, division, print_function

import logging

import rq.timeouts
import rq.worker

log = logging.getLogger("rq.worker")


class NeverTimeout(rq.timeouts.BaseDeathPenalty):
    """Do-nothing object that never times out.

    This is part of the :class:`buildcat.worker.NoForkWorker` implementation,
    since the latter provides no way to interrupt a running job.
    """
    def setup_death_penalty(self):
        log.warning("Job will never timeout.")

    def cancel_death_penalty(self):
        pass


class NoForkWorker(rq.worker.SimpleWorker):
    """RQ worker class that does not fork.

    The default RQ worker class forks to handle each job for reliability, so that
    the worker process can keep running even if the job causes the child process to crash.

    Unfortunately, Python does not support :func:`os.fork` on Windows, making this alternative
    implementation necessary.  You should use this class when starting workers on Windows for use with Buildcat:

        $ rq worker -w buildcat.worker.NoForkWorker
    """
    death_penalty_class = NeverTimeout

