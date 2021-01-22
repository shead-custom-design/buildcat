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

"""Functionality for testing the buildcat installation and setup.
"""

from __future__ import absolute_import, division, print_function

import getpass
import os
import socket
import sys

import rq

import buildcat


def ping():
    """Returns information about a worker.

    Useful for testing that the system is functioning::

        q = buildcat.queue.Queue()
        job = q.submit("buildcat.test.ping")
        print(job.wait())
    """
    return {
        "host": socket.gethostname(),
        "pid": os.getpid(),
        "platform": sys.platform,
        "python": sys.version,
        "prefix": sys.prefix,
        "root": os.getcwd(),
        "user": getpass.getuser(),
    }


def message(msg):
    """Logs a message on a worker.

    Useful for testing that the system is functioning::

        q = buildcat.queue.Queue()
        q.submit("buildcat.test.log", "Hello, World!")

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

        q = buildcat.queue.Queue()
        q.submit("buildcat.test.spawn", 3)

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

        q = buildcat.queue.Queue()
        q.submit("buildcat.test.raise_exception", NotImplementedError())

    The worker that handles this job will raise the given exception and move
    the job to the failed queue, but should continue running.

    Parameters
    ----------
    e: exception object, required
        The exception to be raised.
    """

    raise e

