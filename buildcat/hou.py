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

"""Functionality for integration with SideFX Houdini.
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
    """Return version and path information describing the worker's local Houdini installation.

    Returns
    -------
    metadata: dict
        A collection of key-value pairs containing information describing the
        local Houdini installation.
    """

    command = [_hython_executable(), "-c", info.code]
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

info.code = """
print("buildcat-houdini-version:", hou.applicationVersionString())
"""


def split_frames(hipfile, rop, frames):
    """Render individual frames from a Houdini .hip file.

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
        q.enqueue("buildcat.hou.render_frame", hipfile, rop, frame)


def render_frames(hipfile, rop, frames):
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
    rop = str(rop)
    start = int(frames[0])
    end = int(frames[1])
    step = int(frames[2])

    code = render_frames.code.format(hipfile=hipfile, rop=rop, start=start, end=end-1, step=step)
    command = [_hython_executable(), "-c", code]
    subprocess.check_call(command)

render_frames.code = """
import hou

hou.hipFile.load({hipfile!r}, suppress_save_prompt=True, ignore_load_warnings=True)
rop = hou.node({rop!r})
rop.render(frame_range=({start},{end},{step}), verbose=False, output_progress=False)
"""


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
    rop = str(rop)
    frame = int(frame)

    code = render_frame.code.format(hipfile=hipfile, rop=rop, frame=frame)
    command = [_hython_executable(), "-c", code]
    subprocess.check_call(command)

render_frame.code = """
import hou

hou.hipFile.load({hipfile!r}, suppress_save_prompt=True, ignore_load_warnings=True)
rop = hou.node({rop!r})
rop.render(frame_range=({frame},{frame}), verbose=False, output_progress=False)
"""

