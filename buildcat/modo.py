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

"""Functionality for integration with Foundry Modo.
"""

import re
import subprocess

import rq

import buildcat


def _modo_executable():
    return buildcat.executable("modo_cl")


def info():
    """Return version and path information describing the worker's local Modo installation.

    Returns
    -------
    metadata: dict
        A collection of key-value pairs containing information describing the
        local Houdini installation.
    """

    command = [_modo_executable()]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, universal_newlines=True)
    stdout, stderr = process.communicate(info.code)
    version = re.search("> : (\d+)", stdout).group(1)

    return {
        "modo": {
            "executable": _modo_executable(),
            "version": version,
        },
    }

info.code = """
query platformservice appversion ?
app.quit
"""

def split_frames(lxofile, frames):
    """Render individual frames from a Modo .lxo file.

    Parameters
    ----------
    lxofile: str, required
        Path to the file to be rendered.
    frames: tuple, required
        Contains the half-open (start, end, step) of frames to be rendered.
    """
    lxofile = str(lxofile)
    start = int(frames[0])
    end = int(frames[1])
    step = int(frames[2])

    q = rq.Queue(rq.get_current_job().origin, connection=rq.get_current_connection())
    for frame in range(start, end, step):
        q.enqueue("buildcat.modo.render_frames", lxofile, (frame, frame+1, 1))


def render_frames(lxofile, frames):
    """Render a range of frames from a Modo .lxo file.

    Parameters
    ----------
    lxofile: str, required
        Path to the file to be rendered.
    frames: tuple, required
        Contains the half-open (start, stop, step) range of frames to be rendered.
    """
    start = int(frames[0])
    stop = int(frames[1])
    step = int(frames[2])

    code = render_frames.code.format(lxofile=lxofile, start=start, stop=stop-1, step=step)
    command = [_modo_executable()]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, universal_newlines=True)
    stdout, stderr = process.communicate(code)

render_frames.code = """
log.toConsole true
log.toConsoleRolling true
scene.open "{lxofile}"
pref.value render.threads auto
select.Item Render
item.channel first {start}
item.channel last {stop}
item.channel step {step}
render.animation {{*}}
app.quit
"""
