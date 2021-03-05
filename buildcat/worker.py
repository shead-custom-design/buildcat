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

"""Functionality for retrieving information about workers.
"""

import getpass
import os
import platform
import socket
import sys

import rq

import buildcat


def info():
    """Returns information about a worker.

    Useful for testing that the system is functioning.

    Returns
    -------
    metadata: :class:`dict`
        A collection of key-value pairs containing information describing the
        local worker.
    """
    uname = platform.uname()

    return {
        "os": {
            "host": uname.node,
            "machine": uname.machine,
            "processor": uname.processor,
            "release": uname.release,
            "system": uname.system,
            "version": uname.version,
        },

        "python": {
            "version": sys.version,
            "prefix": sys.prefix,
        },

        "worker": {
            "pid": os.getpid(),
            "root": os.getcwd(),
            "user": getpass.getuser(),
            "version": buildcat.__version__,
        },
    }
