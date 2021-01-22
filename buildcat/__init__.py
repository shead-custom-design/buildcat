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

import logging
import platform
import os

__version__ = "0.3.0-dev"

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


def executable(name):
    return f"{name}.exe" if is_wsl() else name


def is_wsl():
    return "Microsoft" in platform.uname().release


#def rooted_path(root, path):
#    if not root:
#        raise Error("Buildcat Root not specified.", "You must specify the path to the Buildcat shared storage directory for this machine.")
#
#    if not (os.path.exists(root) and os.path.isdir(root)):
#        raise Error("Buildcat Root path does not exist.", "The Buildcat shared storage location must be an existing directory.")
#
#    if not os.path.isabs(root):
#        raise Error("Buildcat Root must be absolute.", "The Buildcat Root path must be an absolute (not relative) path.")
#
#    if not os.path.isabs(path):
#        raise Error("Internal error.", "The path must be an absolute (not relative) path.")
#
#    if not path.startswith(root):
#        raise Error("File stored outside Buildcat Root.", "This file and its assets must be saved to the Buildcat shared storage location to be rendered.")
#    path = os.path.join("$BUILDCAT_ROOT", os.path.relpath(path, root))
#
#    return path

