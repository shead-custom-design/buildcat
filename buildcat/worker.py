# Copyright 2018 Timothy M. Shead
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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


