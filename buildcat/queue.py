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


import pprint
import time

import redis
import rq

import buildcat


class Job(object):
    def __init__(self, connection, job):
        self._connection = connection
        self._job = job

    @property
    def result(self):
        return self._job.result

    def wait(self):
        while True:
            if self._job.is_failed:
                fulljob = rq.job.Job.fetch(self._job.id, connection=self._connection)
                print(fulljob, fulljob.exc_info)
                raise buildcat.Error("Job failed.", "")
            if self._job.result is not None:
                return self._job.result
            time.sleep(0.5)


class Queue(object):
    def __init__(self, queue="default", host="127.0.0.1", port=6379, timeout=5):
        if not host:
            raise buildcat.Error(
                message="Server host not specified.",
                description="You must specify the IP address or hostname of the Buildcat server.",
                )
        try:
            self._connection = redis.Redis(host=host, port=port, socket_timeout=timeout)
            self._connection.ping()
        except redis.exceptions.TimeoutError:
            raise buildcat.Error(
                message="Couldn't connect to server.",
                description="Verify that the Buildcat server is listening at {} port {}.".format(host, port),
                )
        except Exception as e:
            raise buildcat.Error(
                message="Couldn't connect to server.",
                description=str(e),
                )

        if not queue:
            raise buildcat.Error(
                message="Server queue not specified.",
                description="You must specify the name of a Buildcat queue.",
                )

        self._queue = rq.Queue(queue, connection=self._connection)

    def submit(self, command, *args, **kwargs):
        if not command:
            raise buildcat.Error(
                message="Command not specified.",
                description="You must specify the name of a Buildcat command.",
                )

        return Job(self._connection, self._queue.enqueue(command, *args, **kwargs))
