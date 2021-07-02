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

"""Integration with Redshift, https://redshift3d.com.
"""

import os
import re

import buildcat


def _redshift_executable():
    return buildcat.executable("redshiftCmdLine")


def info():
    """Return information describing the worker's local Redshift installation.

    Environment Variables
    ---------------------
    PATH: required
        Your PATH environment variable *must* be configured so that the worker
        can run the `redshiftCmdLine` executable.

    Returns
    -------
    metadata: dict
        A collection of key-value pairs containing a description of the
        Redshift installation on the machine where the job was run.
    """

    command = [_redshift_executable(), "--version"]

    result = buildcat.info()
    result.update({
        "redshift": {
            "executable": _redshift_executable(),
            "version": re.sub(b"\s+", b" ", buildcat.check_output(command)),
        },
    })
    return result


def render(rsfile):
    """Render a Redshift archive (.rs) file.

    Parameters
    ----------
    rsfile: :class:`str`, required
        Relative path of the file to be rendered.

    Environment Variables
    ---------------------
    BUILDCAT_REDSHIFT_GPU: optional
        Whitespace-delimited list of GPU indices to use for rendering.  Default: use all GPUs.
    PATH: required
        Your PATH environment variable *must* be configured so that the worker
        can run the `redshiftCmdLine` executable.
    """

    command = [_redshift_executable(), rsfile]
    for gpu in os.environ.get("BUILDCAT_REDSHIFT_GPU", "").split():
        command += ["-gpu", gpu]

    buildcat.check_call(command)

