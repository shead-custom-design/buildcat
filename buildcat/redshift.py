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

"""Functionality for integration with Redshift, https://redshift3d.com.
"""

import os
import subprocess

import buildcat


def _redshift_executable():
    return buildcat.executable("redshiftCmdLine")


def info():
    """Return version and path information describing the worker's local Redshift installation.

    Returns
    -------
    metadata: dict
        A collection of key-value pairs containing information describing the
        local Redshift installation.
    """

    command = [_redshift_executable(), "--version"]
    result = {
        "redshift": _redshift_executable(),
        "redshift-version": subprocess.check_output(command),
        }
    return result


def render(rsfile):
    command = [_redshift_executable(), rsfile]
    subprocess.check_call(command)
    return True

