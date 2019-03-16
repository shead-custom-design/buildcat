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

"""Functionality for integration with SideFX Houdini.
"""

from __future__ import absolute_import, division, print_function

import json
import subprocess
import time

import buildcat
import buildcat.environment


def _hython_executable():
    return "hython"


def metadata():
    """Return version and path information describing the worker's local Houdini installation.

    Returns
    -------
    metadata: dict
        A collection of key-value pairs containing information describing the
        local Houdini installation.
    """

    command = [_hython_executable(), "-c", metadata.code]
    result = json.loads(subprocess.check_output(command))
    return result

metadata.code = """
import json
import sys
json.dump({
    "name": hou.applicationName(),
    "version": hou.applicationVersionString(),
}, sys.stdout)
"""


def render(hipfile, rop, frames):
    """Render a range of frames from a Houdini .hip file.

    Parameters
    ----------
    hipfile: str, required
        Path to the file to be rendered.
    rop: str, required
        Absolute path of the ROP node to use for rendering.
    frames: tuple, required
        Contains the half-open range of frames to be rendered.
    """
    start, end = frames

    q = buildcat.environment.queue()
    for frame in range(start, end):
        q.enqueue("buildcat.hou.render_frame", hipfile, rop, frame)


def render_frame(hipfile, rop, frame):
    """Render a single frame from a Houdini .hip file.

    Parameters
    ----------
    hipfile: str, required
        Path to the file to be rendered.
    rop: str, required
        Absolute path of the ROP node to use for rendering.
    frame: int, required
        The frame to be rendered.
    """


