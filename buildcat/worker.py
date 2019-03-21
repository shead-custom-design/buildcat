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

"""Provides enhanced RQ worker functionality.
"""

from __future__ import absolute_import, division, print_function

import os

import rq.timeouts
import rq.worker

import buildcat


class NeverTimeout(rq.timeouts.BaseDeathPenalty):
    """Do-nothing object that never times out.

    This is part of the :class:`buildcat.worker.Worker` implementation on
    Windows, since the latter does not provide os.fork, and thus has no way to
    interrupt a running job.
    """
    def setup_death_penalty(self):
        """Do-nothing implementation."""
        buildcat.log.warning("Job will never timeout.")

    def cancel_death_penalty(self):
        """Do-nothing implementation."""
        pass


if hasattr(os, "fork"): # Operating systems with fork()
    worker_base = rq.worker.Worker
    death_penalty_class = rq.timeouts.UnixSignalDeathPenalty
else: # Operating systems without fork(), such as Windows
    worker_base = rq.worker.SimpleWorker
    death_penalty_class = NeverTimeout


class Worker(worker_base):
    """Enhanced RQ worker class for use by Buildcat.

    The default RQ worker class forks to handle each job for reliability, so
    that the worker process can keep running even if the job causes the child
    process to crash.

    Unfortunately, Python does not support :func:`os.fork` on Windows, making
    this alternative implementation necessary.  You must always use this class
    when starting workers for use with Buildcat:

        $ rq worker -w buildcat.worker.Worker
    """
    death_penalty_class = death_penalty_class


