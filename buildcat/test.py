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

import getpass
import os
import socket

import rq

import buildcat


def ping():
    """Returns information about a worker.

    Useful for testing that the system is functioning::

        q = buildcat.queue.Queue()
        job = q.submit("buildcat.test.ping")
        while True:
            if job.result != None:
                print(job.result)
                break
            sleep(0.1)
    """
    return {
        "host": socket.gethostname(),
        "user": getpass.getuser(),
        "root": os.getcwd(),
        "pid": os.getpid(),
    }


def message(msg):
    """Logs a message on a worker.

    Useful for testing that the system is functioning::

        q = rq.Queue(connection=redis.Redis())
        q.enqueue("buildcat.test.log", "Hello, World!")

    After which the given message will appear in the output of the worker that
    handles the job.

    Parameters
    ----------
    msg: str, required
        The message to be logged.
    """

    buildcat.log.info(msg)


def spawn(count):
    """Spawns additional jobs from a worker.

    Useful for verifying that a job handler can spawn additional jobs::

        q = rq.Queue(connection=redis.Redis())
        q.enqueue("buildcat.test.spawn", 3)

    The spawn job will be handled by a worker, which will spawn 3 additional
    :func:`buildcat.test.log` jobs, which will be handled subsequently.

    Parameters
    ----------
    count: int, required
        Number of new jobs to create.
    """

    for index in range(count):
        rq.Queue(connection=rq.get_current_connection()).enqueue("buildcat.test.log", "Job-{}".format(index))


def raise_exception(e):
    """Raise an exception.

    Useful for testing the reliability of workers::

        q = rq.Queue(connection=redis.Redis())
        q.enqueue("buildcat.test.raise_exception", NotImplementedError())

    The worker that handles this job will raise the given exception and move
    the job to the failed queue, but should continue running.

    Parameters
    ----------
    e: exception object, required
        The exception to be raised.
    """

    raise e

