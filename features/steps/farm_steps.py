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

from behave import *

import os
import pprint
import subprocess
import signal
import tempfile
import time

import buildcat
import test


@given(u'a buildcat server')
def step_impl(context):
    def stop_server(context):
        context.server.send_signal(signal.SIGINT)
        context.server.wait(timeout=5)

    context.storage = os.path.join(tempfile.mkdtemp(), "buildcat.aof")
    context.server = subprocess.Popen(["buildcat", "server", "--storage", context.storage])
    context.add_cleanup(stop_server, context)
    while True:
        try:
            connection = buildcat.connect()
            break
        except:
            time.sleep(0.1)


@given(u'a buildcat worker')
def step_impl(context):
    def stop_worker(context):
        context.workers[-1].send_signal(signal.SIGINT)
        context.workers[-1].wait(timeout=5)

    context.workers = [subprocess.Popen(["buildcat", "worker", "--no-fork"])]
    context.add_cleanup(stop_worker, context)


@when(u'submitting a {job} job')
def step_impl(context, job):
    job = eval(job)
    connection, queue = buildcat.queue()
    context.job = buildcat.submit(queue, job)


@then(u'the job count for the {queue} queue should be {count}')
def step_impl(context, count, queue):
    queue = eval(queue)
    count = eval(count)
    connection, queue = buildcat.queue(queue=queue)
    test.assert_equal(len(queue), count)


@then(u'the job should return worker info')
def step_impl(context):
    connection = buildcat.connect()
    result = buildcat.wait(connection=connection, job=context.job)
    for key in ["os", "python", "worker"]:
        test.assert_in(key, result)
    for key in ["host", "machine", "processor", "release", "system", "version"]:
        test.assert_in(key, result["os"])
    for key in ["prefix", "version"]:
        test.assert_in(key, result["python"])
    for key in ["pid", "root", "user"]:
        test.assert_in(key, result["worker"])
