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

"""Provides the Buildcat public API."""

__version__ = "0.3.0-dev"

import logging
import platform
import os
import time

import redis
import rq


formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s:%(name)s:%(message)s", datefmt="%H:%M:%S")

handler = logging.StreamHandler()
handler.setFormatter(formatter)

log = logging.getLogger(__name__)
log.setLevel(os.environ.get("BUILDCAT_LOG_LEVEL", logging.INFO))
log.addHandler(handler)

class Error(Exception):
    """Base class for all Buildcat exceptions.

    Parameters
    ----------
    message: str, required
        Short message describing the failure.
    description: str, required
        Detailed description of the failure, including possible remediations.
    """
    def __init__(self, message, description):
        self.message = message
        self.description = description

    def __repr__(self):
        return "<buildcat.Error message={!r} description={!r}>".format(self.message, self.description)


def connect(*, host="127.0.0.1", port=6379, timeout=5):
    if not host:
        raise Error(
            message="Server host not specified.",
            description="You must specify the IP address or hostname of the Buildcat server.",
            )
    try:
        connection = redis.Redis(host=host, port=port, socket_timeout=timeout)
        connection.ping()
    except redis.exceptions.TimeoutError:
        raise Error(
            message="Couldn't connect to server.",
            description="Verify that the Buildcat server is listening at {} port {}.".format(host, port),
            )
    except Exception as e:
        raise Error(
            message="Couldn't connect to server.",
            description=str(e),
            )
    return connection


def executable(name):
    return f"{name}.exe" if is_wsl() else name


def is_wsl():
    return "microsoft" in platform.uname().release.lower()


def queue(*, queue="default", host="127.0.0.1", port=6379, timeout=5):
    if not queue:
        raise Error(
            message="Server queue not specified.",
            description="You must specify the name of a Buildcat queue.",
            )

    connection = connect(host=host, port=port, timeout=timeout)
    return connection, rq.Queue(queue, connection=connection)


def require_relative_path(path, description):
    if os.path.isabs(path):
        raise Error("Path must be relative.", description)
    return path


def root():
    return os.getcwd()


def submit(queue, command, *args, **kwargs):
    if not command:
        raise Error(
            message="Command not specified.",
            description="You must specify the name of a Buildcat command.",
            )

    return queue.enqueue(command, *args, **kwargs)


def wait(*, connection, job):
    while True:
        if job.is_failed:
            fulljob = rq.job.Job.fetch(job.id, connection=connection)
            print(fulljob, fulljob.exc_info)
            raise Error("Job failed.", "")
        if job.result is not None:
            return job.result
        time.sleep(0.5)

