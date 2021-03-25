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

"""Integration with SideFX Houdini, https://sidefx.com.
"""

import json
import os
import subprocess
import time

import rq

import buildcat


def _hython_executable():
    return buildcat.executable("hython")


def info():
    """Return information describing the worker's local Houdini installation.

    Environment Variables
    ---------------------
    PATH: required
        Your PATH environment variable *must* be configured so that the worker
        can run the `hython` executable.

    Returns
    -------
    metadata: :class:`dict`
        A collection of key-value pairs containing a description of the
        Houdini installation on the machine where the job was run.
    """

    code = """from __future__ import print_function; print("buildcat-houdini-version:", hou.applicationVersionString())"""
    command = [_hython_executable(), "-c", code]
    version = ""
    for line in subprocess.check_output(command).decode("UTF8").splitlines():
        if line.startswith("buildcat-houdini-version: "):
            version = line.split(sep=" ", maxsplit=1)[1]
    return {
        "houdini": {
            "executable": _hython_executable(),
            "version": version,
            },
        }


def render_frames(hipfile, rop, frames):
    """Render a range of frames from a Houdini .hip file.

    Environment Variables
    ---------------------
    PATH: required
        Your PATH environment variable *must* be configured so that the worker
        can run the `hython` executable.

    Parameters
    ----------
    hipfile: :class:`str`, required
        Path to the file to be rendered.
    rop: :class:`str`, required
        Absolute path of the ROP node to use for rendering.
    frames: :class:`tuple` of threeintegers, required
        Contains the half-open (start, end, step) of frames to be rendered.
    """
    hipfile = str(hipfile)
    rop = str(rop)
    start = int(frames[0])
    end = int(frames[1])
    step = int(frames[2])

    code = f"""
import hou

hou.hipFile.load({hipfile!r}, suppress_save_prompt=True, ignore_load_warnings=True)
rop = hou.node({rop!r})
rop.render(frame_range=({start},{end-1},{step}), verbose=False, output_progress=False)
"""
    command = [_hython_executable(), "-c", code]
    subprocess.check_call(command)


def split_frames(hipfile, rop, frames):
    """Render a range of frames from a Houdini .hip file as individual jobs.

    Parameters
    ----------
    hipfile: str, required
        Path to the file to be rendered.
    rop: str, required
        Absolute path of the ROP node to use for rendering.
    frames: tuple, required
        Contains the half-open (start, end, step) of frames to be rendered.
    """
    hipfile = str(hipfile)
    rop = str(rop)
    start = int(frames[0])
    end = int(frames[1])
    step = int(frames[2])

    q = rq.Queue(rq.get_current_job().origin, connection=rq.get_current_connection())
    for frame in range(start, end, step):
        q.enqueue("buildcat.hou.render_frames", hipfile, rop, (frame, frame+1, 1))


